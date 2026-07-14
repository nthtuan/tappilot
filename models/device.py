from enum import Enum
from typing import Optional, Deque
from collections import deque
import threading
from dataclasses import dataclass, field


class DeviceStatus(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


@dataclass
class Device:
    uuid: str
    name: str
    ip: str
    port: int
    status: DeviceStatus = DeviceStatus.DISCONNECTED
    socket: Optional[object] = None
    command_queue: Deque[dict] = field(default_factory=deque)
    worker_thread: Optional[threading.Thread] = None
    heartbeat_thread: Optional[threading.Thread] = None
    is_running: bool = False
    console_messages: list = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def add_console_message(self, message: str):
        with self.lock:
            self.console_messages.append(message)

    def get_console_messages(self) -> list:
        with self.lock:
            return self.console_messages.copy()
