import tkinter as tk
from download_video import download_video
from download_comments import download_comments
from video_info import fetch_video_info

def main():
    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("400x400")

    url_label = tk.Label(root, text="Enter YouTube URL:")
    url_label.pack(pady=10)
    
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=10)

    # Download video
    download_button = tk.Button(root, text="Download Video", command=lambda: download_video(url_entry.get(), root))
    download_button.pack(pady=10)

    # Download comments
    download_comments_button = tk.Button(root, text="Download Comments", command=lambda: download_comments(url_entry.get(), root))
    download_comments_button.pack(pady=10)

    # Fetch video info
    fetch_info_button = tk.Button(root, text="Fetch Video Info", command=lambda: fetch_video_info(url_entry.get(), root))
    fetch_info_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
