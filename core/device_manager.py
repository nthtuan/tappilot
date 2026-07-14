from typing import List, Dict, Optional
from models import Device, DeviceStatus
from .logger import Logger
from .config_manager import ConfigManager
from .network_manager import NetworkManager
from .script_manager import ScriptManager


class DeviceManager:
    _instance: Optional["DeviceManager"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if DeviceManager._initialized:
            return
        DeviceManager._initialized = True

        self.logger = Logger()
        self.config = ConfigManager()
        self.script_manager = ScriptManager()
        self.network_managers: Dict[str, NetworkManager] = {}
        self._initialize_devices()

    def _initialize_devices(self):
        for device in self.config.devices:
            self.script_manager.register_lua_engine(device.uuid, lambda msg: device.add_console_message(msg))

    def get_device(self, uuid: str) -> Optional[Device]:
        for device in self.config.devices:
            if device.uuid == uuid:
                return device
        return None

    def connect_device(self, uuid: str) -> bool:
        device = self.get_device(uuid)
        if not device:
            self.logger.warning(f"Device {uuid} not found")
            return False
        if device.status == DeviceStatus.CONNECTED:
            self.logger.info(f"Device {device.name} already connected")
            return True

        net_manager = NetworkManager(device, self._on_message)
        self.network_managers[uuid] = net_manager
        net_manager.start()
        return True

    def disconnect_device(self, uuid: str) -> bool:
        if uuid not in self.network_managers:
            return False
        self.network_managers[uuid].stop()
        del self.network_managers[uuid]
        return True

    def connect_all(self):
        for device in self.config.devices:
            self.connect_device(device.uuid)

    def disconnect_all(self):
        for uuid in list(self.network_managers.keys()):
            self.disconnect_device(uuid)

    def reconnect_device(self, uuid: str) -> bool:
        self.disconnect_device(uuid)
        return self.connect_device(uuid)

    def reconnect_all(self):
        for uuid in list(self.network_managers.keys()):
            self.reconnect_device(uuid)

    def send_command(self, uuid: str, command: dict):
        if uuid in self.network_managers:
            self.network_managers[uuid].send_message_sync(command)

    def broadcast_command(self, command: dict):
        for uuid in self.network_managers:
            self.send_command(uuid, command)

    def run_script(self, uuid: str, script_name: str) -> bool:
        if self.script_manager.run_script(uuid, script_name):
            self.send_command(uuid, {"type": "run", "name": script_name})
            return True
        return False

    def stop_script(self, uuid: str, script_name: str) -> bool:
        if self.script_manager.stop_script(uuid, script_name):
            self.send_command(uuid, {"type": "stop", "name": script_name})
            return True
        return False

    def run_all_scripts(self, script_name: str):
        for uuid in self.network_managers:
            self.run_script(uuid, script_name)

    def stop_all_scripts(self, script_name: str):
        for uuid in self.network_managers:
            self.stop_script(uuid, script_name)

    def _on_message(self, device: Device, message: dict):
        self.logger.info(f"Received message from {device.name}: {message}")
