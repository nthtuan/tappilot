from typing import List, Optional
import os
from .storage import Storage
from .logger import Logger
from .utils import generate_uuid
from models import Device, DeviceStatus, Settings


class ConfigManager:
    _instance: Optional["ConfigManager"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if ConfigManager._initialized:
            return
        ConfigManager._initialized = True

        self.logger = Logger()
        self.settings_storage = Storage("settings.json")
        self.devices_storage = Storage("devices.json")
        self.settings = self._load_settings()
        self.devices = self._load_devices()

    def _load_settings(self) -> Settings:
        data = self.settings_storage.load()
        if data:
            return Settings(**data)
        return Settings()

    def save_settings(self) -> bool:
        data = {
            "theme": self.settings.theme,
            "language": self.settings.language,
            "window_width": self.settings.window_width,
            "window_height": self.settings.window_height,
            "window_x": self.settings.window_x,
            "window_y": self.settings.window_y,
            "heartbeat_interval": self.settings.heartbeat_interval,
            "reconnect_attempts": self.settings.reconnect_attempts,
            "reconnect_delay": self.settings.reconnect_delay,
            "auto_update": self.settings.auto_update,
            "cache_enabled": self.settings.cache_enabled,
            "log_level": self.settings.log_level
        }
        success = self.settings_storage.save(data)
        if success:
            self.logger.info("Settings saved successfully")
        else:
            self.logger.error("Failed to save settings")
        return success

    def _load_devices(self) -> List[Device]:
        devices_data = self.devices_storage.load()
        devices = []
        if devices_data:
            for dev_data in devices_data:
                device = Device(
                    uuid=dev_data.get("uuid", generate_uuid()),
                    name=dev_data.get("name", "Unknown"),
                    ip=dev_data.get("ip", "127.0.0.1"),
                    port=dev_data.get("port", 8080),
                    status=DeviceStatus.DISCONNECTED
                )
                devices.append(device)
        return devices

    def save_devices(self) -> bool:
        devices_data = []
        for device in self.devices:
            devices_data.append({
                "uuid": device.uuid,
                "name": device.name,
                "ip": device.ip,
                "port": device.port
            })
        success = self.devices_storage.save(devices_data)
        if success:
            self.logger.info("Devices saved successfully")
        else:
            self.logger.error("Failed to save devices")
        return success

    def add_device(self, name: str, ip: str, port: int) -> Device:
        device = Device(
            uuid=generate_uuid(),
            name=name,
            ip=ip,
            port=port
        )
        self.devices.append(device)
        self.save_devices()
        self.logger.info(f"Added new device: {name} ({ip}:{port}")
        return device

    def remove_device(self, uuid: str) -> bool:
        for i, device in enumerate(self.devices):
            if device.uuid == uuid:
                self.devices.pop(i)
                self.save_devices()
                self.logger.info(f"Removed device: {device.name}")
                return True
        self.logger.warning(f"Device with UUID {uuid} not found")
        return False

    def export_devices(self, filepath: str) -> bool:
        try:
            devices_data = []
            for device in self.devices:
                devices_data.append({
                    "uuid": device.uuid,
                    "name": device.name,
                    "ip": device.ip,
                    "port": device.port
                })
            import orjson
            with open(filepath, "wb") as f:
                f.write(orjson.dumps(devices_data, option=orjson.OPT_INDENT_2))
            self.logger.info(f"Devices exported to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export devices: {e}")
            return False

    def import_devices(self, filepath: str) -> bool:
        try:
            import orjson
            with open(filepath, "rb") as f:
                devices_data = orjson.loads(f.read())
            for dev_data in devices_data:
                device = Device(
                    uuid=dev_data.get("uuid", generate_uuid()),
                    name=dev_data.get("name", "Unknown"),
                    ip=dev_data.get("ip", "127.0.0.1"),
                    port=dev_data.get("port", 8080),
                    status=DeviceStatus.DISCONNECTED
                )
                self.devices.append(device)
            self.save_devices()
            self.logger.info(f"Devices imported from {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to import devices: {e}")
            return False
