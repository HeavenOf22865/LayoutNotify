import os
import threading
import tomllib
from pathlib import Path
from time import sleep

import customtkinter as ctk
import win32api
import win32gui
import win32process

root = None
label = None
layout_id_buffer = ""
layouts = {}


def load_layouts_from_config():
    config_dir = Path.home() / ".config" / "LayoutNotify"
    config_path = config_dir / "config.toml"

    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        default_config = '[layouts]\n"1033" = "EN-en"\n"1049" = "RU-ru"\n'
        config_path.write_text(default_config, encoding="utf-8")

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    return config["layouts"]


def get_layout(layouts):
    hwnd = win32gui.GetForegroundWindow()
    thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
    layout_id_full = win32api.GetKeyboardLayout(thread_id)
    layout_id = str(layout_id_full & 0xFFFF)
    layout = layouts.get(layout_id, "")
    return layout, layout_id


def hide_window():

    if root:
        root.withdraw()


def show_notification(layout):
    if label and root:
        label.configure(text=layout)

        root.update_idletasks()
        width = root.winfo_reqwidth()
        height = root.winfo_reqheight()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = screen_height - 150
        root.geometry(f"{width}x{height}+{x}+{y}")

        root.deiconify()
        root.after(1000, hide_window)


def check_layout():
    global layout_id_buffer
    current_layout, current_layout_id = get_layout(layouts)
    if current_layout_id != layout_id_buffer:
        layout_id_buffer = current_layout_id
        show_notification(current_layout)

    if root:
        root.after(100, check_layout)


def main():
    global root, label, layouts, layout_id_buffer

    layouts = load_layouts_from_config()
    _, layout_id_buffer = get_layout(layouts)

    root = ctk.CTk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-toolwindow", True)
    root.attributes("-alpha", 0.75)
    root.configure(fg_color="#2B2B2B")
    root.withdraw()

    label = ctk.CTkLabel(
        root,
        text="",
        font=("Arial", 18, "bold"),
        text_color="white",
        padx=20,
        pady=10,
    )
    label.pack()

    root.after(100, check_layout)
    root.mainloop()


if __name__ == "__main__":
    main()
