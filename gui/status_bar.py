import customtkinter as ctk


class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.status_label = ctk.CTkLabel(self, text="Ready")
        self.status_label.pack(side="left", padx=10, pady=5)

    def set_status(self, text: str):
        self.status_label.configure(text=text)
