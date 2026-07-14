import customtkinter as ctk
from typing import Callable, Optional
from models import Device, DeviceStatus
from core import DeviceManager


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, device_selected_callback: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.device_manager = DeviceManager()
        self.device_selected_callback = device_selected_callback
        self.selected_device_uuid: Optional[str] = None
        self.device_buttons: dict = {}
        self._create_widgets()
        self._refresh_devices()

    def _create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Devices", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=10, padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def _refresh_devices(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.device_buttons.clear()

        for device in self.device_manager.config.devices:
            btn = ctk.CTkButton(self.scroll_frame, text=device.name,
                                command=lambda d=device: self._on_device_selected(d.uuid),
                                fg_color=self._get_status_color(device.status))
            btn.pack(pady=2, fill="x")
            self.device_buttons[device.uuid] = btn

    def _get_status_color(self, status: DeviceStatus) -> str:
        if status == DeviceStatus.CONNECTED:
            return "green"
        elif status == DeviceStatus.CONNECTING or status == DeviceStatus.RECONNECTING:
            return "yellow"
        elif status == DeviceStatus.ERROR:
            return "red"
        else:
            return "gray"

    def _on_device_selected(self, uuid: str):
        self.selected_device_uuid = uuid
        if self.device_selected_callback:
            self.device_selected_callback(uuid)
        self._update_button_states()

    def _update_button_states(self):
        for uuid, btn in self.device_buttons.items():
            if uuid == self.selected_device_uuid:
                btn.configure(fg_color="blue")
            else:
                device = self.device_manager.get_device(uuid)
                if device:
                    btn.configure(fg_color=self._get_status_color(device.status))

    def refresh(self):
        self._refresh_devices()
