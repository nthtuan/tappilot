import customtkinter as ctk
from typing import Optional
from models import Device
from core import DeviceManager, ScriptManager


class TabManager(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.device_manager = DeviceManager()
        self.script_manager = ScriptManager()
        self.device_tabs: dict = {}
        self._create_default_tabs()

    def _create_default_tabs(self):
        self.add("Scripts")
        self._setup_scripts_tab()
        self.add("Logs")
        self._setup_logs_tab()

    def _setup_scripts_tab(self):
        tab = self.tab("Scripts")
        self.scripts_listbox = ctk.CTkScrollableFrame(tab)
        self.scripts_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.upload_script_btn = ctk.CTkButton(tab, text="Upload Script")
        self.upload_script_btn.pack(side="left", padx=10, pady=10)

        self.refresh_scripts()

    def _setup_logs_tab(self):
        tab = self.tab("Logs")
        self.logs_text = ctk.CTkTextbox(tab)
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.export_logs_btn = ctk.CTkButton(tab, text="Export Logs")
        self.export_logs_btn.pack(side="left", padx=10, pady=10)

    def add_device_tab(self, device: Device):
        if device.uuid in self.device_tabs:
            return
        tab_name = device.name
        self.add(tab_name)
        tab = self.tab(tab_name)
        self.device_tabs[device.uuid] = tab
        self._setup_device_tab(tab, device)
        self.set(tab_name)

    def _setup_device_tab(self, tab, device: Device):
        console_frame = ctk.CTkFrame(tab)
        console_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(console_frame, text="Console:").pack(anchor="w", padx=5, pady=5)
        console_text = ctk.CTkTextbox(console_frame)
        console_text.pack(fill="both", expand=True, padx=5, pady=5)

        controls_frame = ctk.CTkFrame(tab)
        controls_frame.pack(fill="x", padx=10, pady=10)

        connect_btn = ctk.CTkButton(controls_frame, text="Connect",
                                    command=lambda: self.device_manager.connect_device(device.uuid))
        connect_btn.pack(side="left", padx=5)

        disconnect_btn = ctk.CTkButton(controls_frame, text="Disconnect",
                                       command=lambda: self.device_manager.disconnect_device(device.uuid))
        disconnect_btn.pack(side="left", padx=5)

        reconnect_btn = ctk.CTkButton(controls_frame, text="Reconnect",
                                      command=lambda: self.device_manager.reconnect_device(device.uuid))
        reconnect_btn.pack(side="left", padx=5)

    def refresh_scripts(self):
        for widget in self.scripts_listbox.winfo_children():
            widget.destroy()
        for script in self.script_manager.get_all_scripts():
            frame = ctk.CTkFrame(self.scripts_listbox)
            frame.pack(fill="x", pady=2)
            lbl = ctk.CTkLabel(frame, text=script.name, anchor="w")
            lbl.pack(side="left", fill="x", expand=True, padx=5)
            run_btn = ctk.CTkButton(frame, text="Run", width=60)
            run_btn.pack(side="left", padx=5)
            stop_btn = ctk.CTkButton(frame, text="Stop", width=60)
            stop_btn.pack(side="left", padx=5)

    def remove_device_tab(self, device: Device):
        if device.uuid in self.device_tabs:
            self.delete(device.name)
            del self.device_tabs[device.uuid]
