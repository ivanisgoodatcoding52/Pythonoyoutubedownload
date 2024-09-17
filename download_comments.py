import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from common import create_progress_window, update_progress, close_progress_window, show_completion_message, ensure_directories
from googleapiclient.discovery import build

# Ensure directories are created
ensure_directories()

# Your API Key here
API_KEY = 'AIzaSyCxoYR72WIhJwZXAxPC7OTKHAWv05VWj40'

def get_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments

def download_comments(video_url, root):
    video_id = video_url.split('v=')[-1]
    
    try:
        progress_window, progress_bar, progress_label = create_progress_window(root, title="Downloading Comments")

        comments = get_comments(video_id, API_KEY)

        if not comments:
            raise Exception("No comments found or failed to extract comments.")

        with open(f"comments/{video_id}_comments.txt", "w", encoding="utf-8") as file:
            for i, comment in enumerate(comments):
                file.write(f"Username: {comment['author']}\n")
                file.write(f"Comment: {comment['text']}\n")
                file.write("-" * 40 + "\n")

                progress = (i + 1) / len(comments) * 100
                update_progress(progress_window, progress_bar, progress_label, progress, f"Downloading comment {i + 1}/{len(comments)}")

        close_progress_window(progress_window)
        show_completion_message(root, f"Downloaded {len(comments)} comments.")

    except Exception as e:
        close_progress_window(progress_window)
        messagebox.showerror("Failed to download comments", f"Reason: {str(e)}")
