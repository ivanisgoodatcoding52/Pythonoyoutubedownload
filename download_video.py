import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from common import create_progress_window, update_progress, close_progress_window, show_completion_message, ensure_directories
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Ensure directories are created
ensure_directories()

# Your API Key here
API_KEY = 'AIzaSyCxoYR72WIhJwZXAxPC7OTKHAWv05VWj40'

def get_channel_info(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            channel_info = response['items'][0]
            return {
                'handle': channel_info['snippet']['title'],
                'subscribers': channel_info['statistics'].get('subscriberCount', 'N/A')
            }
        else:
            return {'handle': 'N/A', 'subscribers': 'N/A'}
    except HttpError as e:
        print(f"An error occurred: {e}")
        return {'handle': 'Error', 'subscribers': 'Error'}

def show_formats(video_url, root):
    ydl_opts = {
        'format': 'bestaudio/best',  # This is a placeholder
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', [])
        
        if not formats:
            messagebox.showerror("Error", "No formats available for this video.")
            return None

        format_details = "\n".join([f"ID: {f['format_id']}, {f.get('format_note', 'N/A')}, {f.get('resolution', 'N/A')}, {f.get('ext', 'N/A')}" for f in formats])
        
        # Create a new window for format selection
        format_window = tk.Toplevel(root)
        format_window.title("Select Format")

        # Create a Text widget to display the formats
        text_widget = tk.Text(format_window, height=15, width=60)
        text_widget.insert(tk.END, f"Available formats:\n\n{format_details}")
        text_widget.pack()

        # Create an Entry widget for format ID input
        tk.Label(format_window, text="Enter the format ID you want to download:").pack(pady=5)
        format_id_entry = tk.Entry(format_window)
        format_id_entry.pack(pady=5)

        selected_format = tk.StringVar()
        
        def on_select_format():
            selected_format.set(format_id_entry.get())
            format_window.destroy()

        # Create a button to confirm the format selection
        tk.Button(format_window, text="Download", command=on_select_format).pack(pady=10)

        # Wait for the format window to close and return the selected format
        root.wait_window(format_window)
        return selected_format.get()

def download_video(video_url, root):
    try:
        # Get the format ID from the user
        format_id = show_formats(video_url, root)
        if not format_id:
            return

        # Create the progress window
        progress_window, progress_bar, progress_label = create_progress_window(root, title="Downloading Video")

        def progress_hook(d):
            if d['status'] == 'downloading':
                percent_complete = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
                update_progress(progress_window, progress_bar, progress_label, percent_complete, f"Downloading {d.get('filename', 'video')}")
            elif d['status'] == 'finished':
                update_progress(progress_window, progress_bar, progress_label, 100, f"Finished downloading {d.get('filename', 'video')}")

        ydl_opts = {
            'format': format_id,  # Use the selected format ID
            'outtmpl': 'videos/%(title)s.%(ext)s',  # Save video to the 'videos' directory
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)

            # Fetch channel info
            channel_info = get_channel_info(info['uploader_id'], API_KEY)

            # Save video info to a file
            with open(f"video_info/{info['id']}_info.txt", "w", encoding="utf-8") as file:
                file.write(f"Title: {info['title']}\n")
                file.write(f"Uploader: {info['uploader']}\n")
                file.write(f"Channel Handle: {channel_info['handle']}\n")
                file.write(f"Subscribers: {channel_info['subscribers']}\n")
                file.write(f"Views: {info['view_count']}\n")
                file.write(f"Likes: {info.get('like_count', 'N/A')}\n")
                file.write(f"Description: {info['description']}\n")

        # Close the progress window
        close_progress_window(progress_window)
        show_completion_message(root, f"Downloaded video '{info['title']}' and saved info.")

    except Exception as e:
        close_progress_window(progress_window)
        messagebox.showerror("Failed to download video", f"Reason: {str(e)}")
