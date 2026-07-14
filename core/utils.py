import os
import uuid as uuidlib


def get_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_uuid() -> str:
    return str(uuidlib.uuid4())
