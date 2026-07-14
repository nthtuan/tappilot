import os
import threading
import time
from typing import Dict, List, Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from .logger import Logger
from .lua_engine import LuaEngine
from .utils import get_project_root


class Script:
    def __init__(self, name: str, filepath: str):
        self.name = name
        self.filepath = filepath
        self.is_running = False
        self.last_modified = os.path.getmtime(filepath) if os.path.exists(filepath) else 0


class ScriptManager:
    _instance: Optional["ScriptManager"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if ScriptManager._initialized:
            return
        ScriptManager._initialized = True

        self.logger = Logger()
        self.scripts_dir = os.path.join(get_project_root(), "scripts")
        os.makedirs(self.scripts_dir, exist_ok=True)
        self.scripts: Dict[str, Script] = {}
        self.lua_engines: Dict[str, LuaEngine] = {}
        self.observer: Optional[Observer] = None
        self.watchdog_thread: Optional[threading.Thread] = None
        self.is_watching = False
        self._load_initial_scripts()

    def _load_initial_scripts(self):
        if os.path.exists(self.scripts_dir):
            for filename in os.listdir(self.scripts_dir):
                if filename.endswith(".lua"):
                    filepath = os.path.join(self.scripts_dir, filename)
                    self.scripts[filename] = Script(filename, filepath)
                    self.logger.info(f"Loaded script: {filename}")

    def register_lua_engine(self, device_uuid: str, log_callback: Optional[Callable[[str], None]] = None):
        if device_uuid not in self.lua_engines:
            engine = LuaEngine(device_uuid, log_callback)
            engine.initialize()
            self.lua_engines[device_uuid] = engine
            self.logger.info(f"Registered Lua engine for device: {device_uuid}")

    def unregister_lua_engine(self, device_uuid: str):
        if device_uuid in self.lua_engines:
            self.lua_engines[device_uuid].stop()
            del self.lua_engines[device_uuid]
            self.logger.info(f"Unregistered Lua engine for device: {device_uuid}")

    def get_script(self, name: str) -> Optional[Script]:
        return self.scripts.get(name)

    def get_all_scripts(self) -> List[Script]:
        return list(self.scripts.values())

    def upload_script(self, name: str, content: str) -> bool:
        try:
            filepath = os.path.join(self.scripts_dir, name)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            self.scripts[name] = Script(name, filepath)
            self.logger.info(f"Uploaded script: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload script {name}: {str(e)}")
            return False

    def run_script(self, device_uuid: str, script_name: str) -> bool:
        engine = self.lua_engines.get(device_uuid)
        script = self.scripts.get(script_name)

        if not engine:
            self.logger.error(f"No Lua engine for device {device_uuid}")
            return False
        if not script:
            self.logger.error(f"Script {script_name} not found")
            return False

        try:
            script.is_running = True
            engine.execute_file(script.filepath)
            self.logger.info(f"Running script {script_name} on device {device_uuid}")
            return True
        except Exception as e:
            script.is_running = False
            self.logger.error(f"Failed to run script {script_name}: {str(e)}")
            return False

    def stop_script(self, device_uuid: str, script_name: str) -> bool:
        script = self.scripts.get(script_name)
        if script:
            script.is_running = False
            self.logger.info(f"Stopped script {script_name} on device {device_uuid}")
            return True
        return False

    def reload_script(self, device_uuid: str, script_name: str) -> bool:
        if self.stop_script(device_uuid, script_name):
            return self.run_script(device_uuid, script_name)
        return False

    def _watchdog_worker(self):
        event_handler = self.ScriptChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.scripts_dir, recursive=False)
        self.observer.start()
        self.logger.info("Script watchdog started")

        while self.is_watching:
            time.sleep(1)

        self.observer.stop()
        self.observer.join()
        self.logger.info("Script watchdog stopped")

    def start_watchdog(self):
        if self.is_watching:
            return
        self.is_watching = True
        self.watchdog_thread = threading.Thread(target=self._watchdog_worker, daemon=True)
        self.watchdog_thread.start()

    def stop_watchdog(self):
        self.is_watching = False
        if self.watchdog_thread and self.watchdog_thread.is_alive():
            self.watchdog_thread.join()

    class ScriptChangeHandler(FileSystemEventHandler):
        def __init__(self, manager: "ScriptManager"):
            self.manager = manager

        def on_modified(self, event):
            if isinstance(event, FileModifiedEvent) and event.src_path.endswith(".lua"):
                filename = os.path.basename(event.src_path)
                self.manager.logger.info(f"Script changed: {filename}")
                # Auto-reload running scripts
                for script in self.manager.scripts.values():
                    if script.name == filename and script.is_running:
                        self.manager.logger.info(f"Auto-reloading script: {filename}")
