import threading
from time import sleep

import customtkinter as ctk
import win32api
import win32gui
import win32process

current_window = None


def get_layout():
    hwnd = win32gui.GetForegroundWindow()

    thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)

    layout_id_full = win32api.GetKeyboardLayout(thread_id)

    layout_id = layout_id_full & 0xFFFF

    if layout_id == 0x0409:
        layout = "EN-en"

    elif layout_id == 0x0419:
        layout = "RU-ru"

    else:
        layout = "Unknown"

    return layout


def show_notification(layout):
    global current_window

    if current_window is not None:
        try:
            current_window.destroy()
        except:
            pass

    root = ctk.CTk()

    current_window = root

    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.75)

    root.configure(fg_color="#2B2B2B")
    label = ctk.CTkLabel(
        root,
        text=layout,
        font=("Arial", 18, "bold"),
        text_color="white",
        padx=20,
        pady=10,
    )
    label.pack()

    root.update_idletasks()

    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = screen_height - 150

    root.geometry(f"{width}x{height}+{x}+{y}")

    root.after(1000, root.destroy)

    root.mainloop()

    if current_window == root:
        current_window = None


def main():
    layout_buffer = get_layout()

    while True:
        current_layout = get_layout()

        if current_layout != layout_buffer:
            layout_buffer = current_layout

            threading.Thread(
                target=show_notification, args=(current_layout,), daemon=True
            ).start()

        sleep(0.1)


if __name__ == "__main__":
    main()
