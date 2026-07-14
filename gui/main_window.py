import customtkinter as ctk
from typing import Optional
from .theme import ThemeManager
from .toolbar import Toolbar
from .sidebar import Sidebar
from .tab_manager import TabManager
from .status_bar import StatusBar
from core import DeviceManager, ConfigManager, ScriptManager, Logger


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TapPilot")
        self.geometry("1200x800")

        self.theme_manager = ThemeManager()
        self.device_manager = DeviceManager()
        self.config = ConfigManager()
        self.script_manager = ScriptManager()
        self.logger = Logger()

        self._apply_window_settings()
        self._create_widgets()
        self._setup_callbacks()
        self._start_update_loop()

    def _apply_window_settings(self):
        if self.config.settings.theme:
            self.theme_manager.apply_theme(self.config.settings.theme)
        if self.config.settings.window_width and self.config.settings.window_height:
            self.geometry(f"{self.config.settings.window_width}x{self.config.settings.window_height}")
        if self.config.settings.window_x and self.config.settings.window_y:
            self.geometry(f"+{self.config.settings.window_x}+{self.config.settings.window_y}")

    def _create_widgets(self):
        self.toolbar = Toolbar(self)
        self.toolbar.pack(fill="x", padx=5, pady=5)

        self.main_paned = ctk.CTkFrame(self)
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)

        self.sidebar = Sidebar(self.main_paned, device_selected_callback=self._on_device_selected)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.tab_manager = TabManager(self.main_paned)
        self.tab_manager.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill="x", padx=5, pady=5)

    def _setup_callbacks(self):
        self.toolbar.set_callbacks(
            add_device=self._add_device,
            connect_all=self.device_manager.connect_all,
            disconnect_all=self.device_manager.disconnect_all,
            run_all=self._run_all_scripts,
            stop_all=self._stop_all_scripts,
            settings=self._open_settings
        )

    def _on_device_selected(self, uuid: str):
        device = self.device_manager.get_device(uuid)
        if device:
            self.tab_manager.add_device_tab(device)

    def _add_device(self):
        dialog = ctk.CTkInputDialog(text="Enter Device Name:", title="Add Device")
        name = dialog.get_input()
        if not name:
            return

        dialog = ctk.CTkInputDialog(text="Enter Device IP:", title="Add Device")
        ip = dialog.get_input()
        if not ip:
            return

        dialog = ctk.CTkInputDialog(text="Enter Device Port:", title="Add Device")
        port = dialog.get_input()
        if not port:
            return
        try:
            port = int(port)
        except ValueError:
            return

        self.config.add_device(name, ip, port)
        self.sidebar.refresh()
        self.status_bar.set_status(f"Added device: {name}")

    def _run_all_scripts(self):
        self.status_bar.set_status("Running all scripts...")
        self.logger.info("Running all scripts")

    def _stop_all_scripts(self):
        self.status_bar.set_status("Stopping all scripts...")
        self.logger.info("Stopping all scripts")

    def _open_settings(self):
        self.status_bar.set_status("Opening settings...")
        # TODO: Implement settings dialog
        pass

    def _start_update_loop(self):
        self.sidebar.refresh()
        self.after(1000, self._start_update_loop)

    def on_closing(self):
        self.config.settings.window_width = self.winfo_width()
        self.config.settings.window_height = self.winfo_height()
        self.config.settings.window_x = self.winfo_x()
        self.config.settings.window_y = self.winfo_y()
        self.config.save_settings()
        self.device_manager.disconnect_all()
        self.destroy()
