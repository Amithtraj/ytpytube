import tkinter as tk
from tkinter import ttk, messagebox
import pytube
from pytube.exceptions import VideoUnavailable, RegexMatchError
import threading

# Improved Readability Material Design Colors
bg_color = "#ECEFF1"  # Light Blue Grey for background
fg_color = "#37474F"  # Dark Blue Grey for input fields
button_color = "#FFC107"  # Amber for buttons
progress_bar_color = "#4CAF50"  # Green for progress bar
text_color = "#263238"  # Deep Blue Grey for text
input_bg_color = "#CFD8DC"  # Lighter Blue Grey for inputs

class YouTubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Video Downloader")
        self.geometry("600x300")
        self.configure(bg=bg_color)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.style.configure('TButton', background=button_color, foreground=text_color, font=('Roboto', 10))
        self.style.configure('TLabel', background=bg_color, foreground=text_color, font=('Roboto', 10))
        self.style.configure('TEntry', foreground=fg_color, fieldbackground=input_bg_color)
        self.style.configure('Horizontal.TProgressbar', troughcolor=bg_color, bordercolor=bg_color, background=progress_bar_color)

        self.init_ui()

    def init_ui(self):
        self.url_label = ttk.Label(self, text="YouTube Video URL:")
        self.url_label.pack(pady=(20, 5))

        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.pack(pady=(0, 10))

        self.quality_label = ttk.Label(self, text="Select Video Quality:")
        self.quality_label.pack(pady=(10, 5))

        # Dropdown for quality selection
        self.quality_var = tk.StringVar()
        self.qualities = ['720p', '480p', '360p', '240p', '144p']
        self.quality_combobox = ttk.Combobox(self, textvariable=self.quality_var, values=self.qualities, state='readonly')
        self.quality_combobox.current(0)  # default to first quality option
        self.quality_combobox.pack(pady=(0, 20))

        self.download_button = ttk.Button(self, text="Download Video", command=self.start_download_thread)
        self.download_button.pack(pady=(0, 20))

        self.progress = ttk.Progressbar(self, style='Horizontal.TProgressbar', length=400, mode='determinate')
        self.progress.pack(pady=(0, 20))

    def start_download_thread(self):
        self.progress['value'] = 0
        download_thread = threading.Thread(target=self.download_youtube_video)
        download_thread.start()

    def download_youtube_video(self):
        video_url = self.url_entry.get()
        desired_resolution = self.quality_var.get()
        output_path = "./"

        try:
            yt = pytube.YouTube(video_url)
            yt.register_on_progress_callback(self.on_progress)
            stream = yt.streams.filter(res=desired_resolution, progressive=True).first()
            if stream:
                stream.download(output_path)
                messagebox.showinfo("Success", f"Video downloaded successfully:\n{stream.default_filename}")
            else:
                messagebox.showerror("Error", "Desired resolution not available.")
        except (VideoUnavailable, RegexMatchError) as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            self.progress['value'] = 0

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        self.progress['value'] = percentage_of_completion
        self.update_idletasks()

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
