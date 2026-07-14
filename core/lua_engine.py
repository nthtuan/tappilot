import threading
from typing import Callable, Optional
from lupa import LuaRuntime
from .logger import Logger


class LuaEngine:
    def __init__(self, device_uuid: str, log_callback: Optional[Callable[[str], None]] = None):
        self.device_uuid = device_uuid
        self.logger = Logger()
        self.log_callback = log_callback
        self.lua: Optional[LuaRuntime] = None
        self.is_running = False
        self.lock = threading.Lock()

    def _redirect_print(self, *args):
        message = " ".join(str(arg) for arg in args)
        self._log(f"[LUA] {message}")

    def _log(self, message: str):
        if self.log_callback:
            self.log_callback(message)
        self.logger.info(f"[{self.device_uuid}] {message}")

    def initialize(self):
        with self.lock:
            if self.lua is not None:
                self.logger.warning("Lua engine already initialized")
                return

            self.lua = LuaRuntime(unpack_returned_tuples=True)
            self.lua.globals()["print"] = self._redirect_print
            self.is_running = True
            self._log("Lua engine initialized")

    def execute(self, code: str) -> Optional[object]:
        with self.lock:
            if not self.lua or not self.is_running:
                self._log("Lua engine not running")
                return None

            try:
                result = self.lua.execute(code)
                return result
            except Exception as e:
                error_msg = f"LUA ERROR: {str(e)}"
                self._log(error_msg)
                return None

    def execute_file(self, filepath: str) -> Optional[object]:
        with self.lock:
            if not self.lua or not self.is_running:
                self._log("Lua engine not running")
                return None

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()
                return self.execute(code)
            except Exception as e:
                error_msg = f"LUA ERROR loading file {filepath}: {str(e)}"
                self._log(error_msg)
                return None

    def stop(self):
        with self.lock:
            if self.lua is None:
                return

            self.is_running = False
            self.lua = None
            self._log("Lua engine stopped")

    def reload(self):
        self.stop()
        self.initialize()
