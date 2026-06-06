import threading
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from app.downloader import download_youtube_audio_as_mp3, DownloadError


class YouTubeMP3App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("YouTube MP3 Downloader")
        self.window.geometry("560x320")
        self.window.resizable(False, False)

        self.bg_color = "#121212"
        self.card_color = "#1E1E1E"
        self.text_color = "#FFFFFF"
        self.secondary_text_color = "#B3B3B3"
        self.accent_color = "#1DB954"
        self.accent_hover_color = "#18A84B"
        self.error_color = "#FF6B6B"

        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Paste a YouTube link and download the MP3.")

        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        self.window.configure(bg=self.bg_color)

    def _build_ui(self):
        container = tk.Frame(self.window, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=28, pady=24)

        title = tk.Label(
            container,
            text="YouTube MP3 Downloader",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            container,
            text="Paste a YouTube URL and save the audio as an MP3 file.",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.secondary_text_color,
        )
        subtitle.pack(anchor="w", pady=(4, 20))

        card = tk.Frame(container, bg=self.card_color)
        card.pack(fill="x", pady=(0, 18))

        input_label = tk.Label(
            card,
            text="YouTube URL",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        input_label.pack(anchor="w", padx=18, pady=(16, 6))

        self.url_entry = tk.Entry(
            card,
            textvariable=self.url_var,
            font=("Segoe UI", 11),
            bg="#2A2A2A",
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
        )
        self.url_entry.pack(fill="x", padx=18, ipady=8)

        self.download_button = tk.Button(
            card,
            text="Download MP3",
            command=self._start_download,
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg="#000000",
            activebackground=self.accent_hover_color,
            activeforeground="#000000",
            relief="flat",
            cursor="hand2",
        )
        self.download_button.pack(fill="x", padx=18, pady=18, ipady=8)

        status = tk.Label(
            container,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.secondary_text_color,
            wraplength=500,
            justify="left",
        )
        status.pack(anchor="w")

        footer = tk.Label(
            container,
            text="Use only with videos you own, public domain content, or content you have permission to download.",
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg="#777777",
            wraplength=500,
            justify="left",
        )
        footer.pack(anchor="w", side="bottom", pady=(16, 0))

    def _start_download(self):
        url = self.url_var.get().strip()

        if not url:
            messagebox.showwarning("Missing URL", "Please enter a YouTube URL.")
            return

        self._set_loading_state(True)

        thread = threading.Thread(
            target=self._download_audio,
            args=(url,),
            daemon=True,
        )
        thread.start()

    def _download_audio(self, url: str):
        try:
            downloads_path = download_youtube_audio_as_mp3(url)
            self.window.after(0, self._on_download_success, downloads_path)

        except DownloadError as error:
            self.window.after(0, self._on_download_error, str(error))

        except Exception:
            self.window.after(
                0,
                self._on_download_error,
                "Unexpected error. Please try again.",
            )

    def _on_download_success(self, downloads_path: Path):
        self._set_loading_state(False)
        self.status_var.set(f"Done! Your MP3 was saved in: {downloads_path.resolve()}")
        messagebox.showinfo("Download complete", "The MP3 file was downloaded successfully.")

    def _on_download_error(self, error_message: str):
        self._set_loading_state(False)
        self.status_var.set(error_message)
        messagebox.showerror("Download failed", error_message)

    def _set_loading_state(self, is_loading: bool):
        if is_loading:
            self.download_button.config(text="Downloading...", state="disabled")
            self.status_var.set("Downloading audio. Please wait...")
        else:
            self.download_button.config(text="Download MP3", state="normal")

    def run(self):
        self.url_entry.focus()
        self.window.mainloop()