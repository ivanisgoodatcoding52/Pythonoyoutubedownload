import tkinter as tk
from tkinter import Toplevel, ttk  # Import ttk for Progressbar
import os

def create_progress_window(root, title="Progress"):
    progress_window = Toplevel(root)
    progress_window.title(title)

    progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack(pady=10)

    progress_label = tk.Label(progress_window, text="Starting...")
    progress_label.pack(pady=10)

    return progress_window, progress_bar, progress_label

def update_progress(progress_window, progress_bar, progress_label, value, text):
    progress_bar['value'] = value
    progress_label['text'] = text
    progress_window.update_idletasks()

def close_progress_window(progress_window):
    progress_window.destroy()

def show_completion_message(root, message):
    completion_window = Toplevel(root)
    completion_window.title("Download Complete")

    label = tk.Label(completion_window, text=message, padx=20, pady=20)
    label.pack()

    button = tk.Button(completion_window, text="OK", command=completion_window.destroy)
    button.pack(pady=10)
def ensure_directories():
    directories = ['videos', 'video_info', 'comments']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
