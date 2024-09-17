import tkinter as tk
from tkinter import messagebox
import yt_dlp
from common import create_progress_window, update_progress, close_progress_window

def fetch_video_info(url, root):
    progress_window, progress_bar, progress_label = create_progress_window(root, title="Fetching Video Info")

    def update_info(data):
        title = data.get('title', 'N/A')
        views = data.get('view_count', 'N/A')
        likes = data.get('like_count', 'N/A')
        description = data.get('description', 'N/A')
        uploader = data.get('uploader', 'N/A')
        subscribers = data.get('uploader_subscriber_count', 'N/A')

        info_text = (
            f"Title: {title}\n"
            f"Views: {views}\n"
            f"Likes: {likes}\n"
            f"Description: {description}\n"
            f"Channel: {uploader}\n"
            f"Subscribers: {subscribers}\n"
        )

        save_video_info_to_txt(info_text)

    def save_video_info_to_txt(info_text):
        try:
            filename = "video_info.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(info_text)
            messagebox.showinfo("Success", f"Video info successfully saved to {filename}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save video info. Reason: {e}")
        finally:
            close_progress_window(progress_window)

    def progress_hook(data):
        update_progress(progress_window, progress_bar, progress_label, 50, "Fetching video info...")

    ydl_opts = {
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            update_info(info)
            update_progress(progress_window, progress_bar, progress_label, 100, "Fetch complete!")
            close_progress_window(progress_window)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch video info. Reason: {e}")
        close_progress_window(progress_window)
