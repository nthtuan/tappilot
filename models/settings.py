from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Settings:
    theme: str = "dark"
    language: str = "vi"
    window_width: int = 1200
    window_height: int = 800
    window_x: int = 0
    window_y: int = 0
    heartbeat_interval: int = 5
    reconnect_attempts: int = 3
    reconnect_delay: int = 2
    auto_update: bool = False
    cache_enabled: bool = True
    log_level: str = "INFO"
