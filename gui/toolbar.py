import customtkinter as ctk
from typing import Callable


class Toolbar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        self.add_device_btn = ctk.CTkButton(self, text="Add Device")
        self.add_device_btn.pack(side="left", padx=5, pady=5)

        self.connect_all_btn = ctk.CTkButton(self, text="Connect All")
        self.connect_all_btn.pack(side="left", padx=5, pady=5)

        self.disconnect_all_btn = ctk.CTkButton(self, text="Disconnect All")
        self.disconnect_all_btn.pack(side="left", padx=5, pady=5)

        self.run_all_btn = ctk.CTkButton(self, text="Run All Scripts")
        self.run_all_btn.pack(side="left", padx=5, pady=5)

        self.stop_all_btn = ctk.CTkButton(self, text="Stop All Scripts")
        self.stop_all_btn.pack(side="left", padx=5, pady=5)

        self.settings_btn = ctk.CTkButton(self, text="Settings")
        self.settings_btn.pack(side="right", padx=5, pady=5)

    def set_callbacks(self, add_device: Callable, connect_all: Callable, disconnect_all: Callable,
                      run_all: Callable, stop_all: Callable, settings: Callable):
        self.add_device_btn.configure(command=add_device)
        self.connect_all_btn.configure(command=connect_all)
        self.disconnect_all_btn.configure(command=disconnect_all)
        self.run_all_btn.configure(command=run_all)
        self.stop_all_btn.configure(command=stop_all)
        self.settings_btn.configure(command=settings)
