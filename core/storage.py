import os
import orjson
from typing import Any, Dict, List, Optional
from .utils import get_project_root


class Storage:
    def __init__(self, filename: str):
        self.config_dir = os.path.join(get_project_root(), "config")
        os.makedirs(self.config_dir, exist_ok=True)
        self.filepath = os.path.join(self.config_dir, filename)

    def load(self) -> Optional[Dict | List]:
        if not os.path.exists(self.filepath):
            return None
        try:
            with open(self.filepath, "rb") as f:
                return orjson.loads(f.read())
        except Exception:
            return None

    def save(self, data: Dict | List) -> bool:
        try:
            with open(self.filepath, "wb") as f:
                f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
            return True
        except Exception:
            return False
