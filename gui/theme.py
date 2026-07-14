import customtkinter as ctk


class ThemeManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if ThemeManager._initialized:
            return
        ThemeManager._initialized = True
        self.current_theme = "dark"
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme: str):
        self.current_theme = theme
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")
