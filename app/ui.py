import os
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from app.downloader import (
    DownloadError,
    download_youtube_audio_as_mp3,
    get_user_downloads_folder,
)


TRANSLATIONS = {
    "en": {
        "app_title": "YouTube MP3 Downloader",
        "subtitle": "Paste a YouTube URL and save the audio as an MP3 file.",
        "language": "Language",
        "youtube_url": "YouTube URL",
        "placeholder_status": "Paste a YouTube link and download the MP3.",
        "download_button": "Download MP3",
        "downloading": "Downloading...",
        "downloading_status": "Downloading audio. Please wait...",
        "open_downloads": "Open downloads folder",
        "download_complete_title": "Download complete",
        "download_complete_message": "The MP3 file was downloaded successfully.",
        "download_done_status": "Done! Your MP3 was saved in:",
        "missing_url_title": "Missing URL",
        "missing_url_message": "Please enter a YouTube URL.",
        "download_failed_title": "Download failed",
        "unexpected_error": "Unexpected error. Please try again.",
        "open_folder_error": "Could not open folder:",
        "footer": "Use only with videos you own, public domain content, or content you have permission to download.",
        "save_location": "Files will be saved directly in your Downloads folder.",
    },
    "es": {
        "app_title": "Descargador de MP3 de YouTube",
        "subtitle": "Pegá un enlace de YouTube y guardá el audio como archivo MP3.",
        "language": "Idioma",
        "youtube_url": "URL de YouTube",
        "placeholder_status": "Pegá un enlace de YouTube y descargá el MP3.",
        "download_button": "Descargar MP3",
        "downloading": "Descargando...",
        "downloading_status": "Descargando audio. Por favor esperá...",
        "open_downloads": "Abrir carpeta de descargas",
        "download_complete_title": "Descarga completa",
        "download_complete_message": "El archivo MP3 se descargó correctamente.",
        "download_done_status": "Listo! Tu MP3 se guardó en:",
        "missing_url_title": "Falta la URL",
        "missing_url_message": "Por favor ingresá una URL de YouTube.",
        "download_failed_title": "Error en la descarga",
        "unexpected_error": "Error inesperado. Por favor intentá de nuevo.",
        "open_folder_error": "No se pudo abrir la carpeta:",
        "footer": "Usar solo con videos propios, contenido de dominio público o contenido que tengas permiso para descargar.",
        "save_location": "Los archivos se guardarán directamente en tu carpeta de Descargas.",
    },
}


LANGUAGE_OPTIONS = {
    "🇺🇸 English": "en",
    "🇪🇸 Español": "es",
}


class YouTubeMP3App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("620x420")
        self.window.minsize(620, 420)
        self.window.resizable(False, False)

        self.bg_color = "#101010"
        self.card_color = "#1C1C1C"
        self.input_color = "#2A2A2A"
        self.text_color = "#FFFFFF"
        self.secondary_text_color = "#B8B8B8"
        self.muted_text_color = "#7A7A7A"
        self.accent_color = "#1DB954"
        self.accent_hover_color = "#18A84B"
        self.button_text_color = "#000000"

        self.current_language = "en"
        self.url_var = tk.StringVar()
        self.language_var = tk.StringVar(value="🇺🇸 English")
        self.status_var = tk.StringVar()
        self.downloads_path = get_user_downloads_folder()

        self.widgets = {}

        self._setup_window()
        self._build_ui()
        self._apply_language()

    def _t(self, key: str) -> str:
        return TRANSLATIONS[self.current_language][key]

    def _setup_window(self):
        self.window.configure(bg=self.bg_color)

    def _build_ui(self):
        container = tk.Frame(self.window, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=30, pady=24)

        top_bar = tk.Frame(container, bg=self.bg_color)
        top_bar.pack(fill="x")

        title_area = tk.Frame(top_bar, bg=self.bg_color)
        title_area.pack(side="left", fill="x", expand=True)

        self.widgets["title"] = tk.Label(
            title_area,
            font=("Segoe UI", 21, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
        )
        self.widgets["title"].pack(anchor="w")

        self.widgets["subtitle"] = tk.Label(
            title_area,
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.secondary_text_color,
        )
        self.widgets["subtitle"].pack(anchor="w", pady=(4, 0))

        language_area = tk.Frame(top_bar, bg=self.bg_color)
        language_area.pack(side="right", anchor="n")

        self.widgets["language_label"] = tk.Label(
            language_area,
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_color,
            fg=self.secondary_text_color,
        )
        self.widgets["language_label"].pack(anchor="w")

        self.language_menu = tk.OptionMenu(
            language_area,
            self.language_var,
            *LANGUAGE_OPTIONS.keys(),
            command=self._change_language,
        )
        self.language_menu.config(
            font=("Segoe UI Emoji", 10, "bold"),
            bg=self.input_color,
            fg=self.text_color,
            activebackground="#333333",
            activeforeground=self.text_color,
            highlightthickness=0,
            relief="flat",
            cursor="hand2",
            width=13,
        )
        self.language_menu["menu"].config(
            font=("Segoe UI Emoji", 10),
            bg=self.input_color,
            fg=self.text_color,
            activebackground=self.accent_color,
            activeforeground=self.button_text_color,
            relief="flat",
        )
        self.language_menu.pack(pady=(5, 0))

        card = tk.Frame(container, bg=self.card_color)
        card.pack(fill="x", pady=(28, 18))

        self.widgets["url_label"] = tk.Label(
            card,
            font=("Segoe UI", 10, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        self.widgets["url_label"].pack(anchor="w", padx=20, pady=(18, 7))

        self.url_entry = tk.Entry(
            card,
            textvariable=self.url_var,
            font=("Segoe UI", 11),
            bg=self.input_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
        )
        self.url_entry.pack(fill="x", padx=20, ipady=9)

        self.widgets["save_location"] = tk.Label(
            card,
            font=("Segoe UI", 9),
            bg=self.card_color,
            fg=self.secondary_text_color,
        )
        self.widgets["save_location"].pack(anchor="w", padx=20, pady=(10, 0))

        self.download_button = tk.Button(
            card,
            command=self._start_download,
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg=self.button_text_color,
            activebackground=self.accent_hover_color,
            activeforeground=self.button_text_color,
            relief="flat",
            cursor="hand2",
        )
        self.download_button.pack(fill="x", padx=20, pady=(18, 10), ipady=9)

        self.open_folder_button = tk.Button(
            card,
            command=self._open_downloads_folder,
            font=("Segoe UI", 10, "bold"),
            bg=self.input_color,
            fg=self.text_color,
            activebackground="#333333",
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
        )
        self.open_folder_button.pack(fill="x", padx=20, pady=(0, 20), ipady=7)

        self.widgets["status"] = tk.Label(
            container,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.secondary_text_color,
            wraplength=540,
            justify="left",
        )
        self.widgets["status"].pack(anchor="w", fill="x")

        self.widgets["footer"] = tk.Label(
            container,
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg=self.muted_text_color,
            wraplength=540,
            justify="left",
        )
        self.widgets["footer"].pack(anchor="w", side="bottom", pady=(18, 0))

    def _apply_language(self):
        self.window.title(self._t("app_title"))

        self.widgets["title"].config(text=self._t("app_title"))
        self.widgets["subtitle"].config(text=self._t("subtitle"))
        self.widgets["language_label"].config(text=self._t("language"))
        self.widgets["url_label"].config(text=self._t("youtube_url"))
        self.widgets["save_location"].config(text=self._t("save_location"))
        self.widgets["footer"].config(text=self._t("footer"))

        self.download_button.config(text=self._t("download_button"))
        self.open_folder_button.config(text=self._t("open_downloads"))

        if not self.status_var.get():
            self.status_var.set(self._t("placeholder_status"))

    def _change_language(self, selected_language: str):
        self.current_language = LANGUAGE_OPTIONS.get(selected_language, "en")

        previous_statuses = [
            TRANSLATIONS["en"]["placeholder_status"],
            TRANSLATIONS["es"]["placeholder_status"],
        ]

        current_status = self.status_var.get()

        self._apply_language()

        if current_status in previous_statuses:
            self.status_var.set(self._t("placeholder_status"))

    def _start_download(self):
        url = self.url_var.get().strip()

        if not url:
            messagebox.showwarning(
                self._t("missing_url_title"),
                self._t("missing_url_message"),
            )
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
            downloads_path = download_youtube_audio_as_mp3(
                url=url,
                output_dir=self.downloads_path,
            )
            self.window.after(0, self._on_download_success, downloads_path)

        except DownloadError as error:
            self.window.after(0, self._on_download_error, str(error))

        except Exception:
            self.window.after(
                0,
                self._on_download_error,
                self._t("unexpected_error"),
            )

    def _on_download_success(self, downloads_path: Path):
        self._set_loading_state(False)
        self.status_var.set(f"{self._t('download_done_status')} {downloads_path.resolve()}")

        messagebox.showinfo(
            self._t("download_complete_title"),
            self._t("download_complete_message"),
        )

    def _on_download_error(self, error_message: str):
        self._set_loading_state(False)
        self.status_var.set(error_message)

        messagebox.showerror(
            self._t("download_failed_title"),
            error_message,
        )

    def _set_loading_state(self, is_loading: bool):
        if is_loading:
            self.download_button.config(text=self._t("downloading"), state="disabled")
            self.status_var.set(self._t("downloading_status"))
        else:
            self.download_button.config(text=self._t("download_button"), state="normal")

    def _open_downloads_folder(self):
        path = self.downloads_path.resolve()

        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", str(path)], check=False)
            else:
                subprocess.run(["xdg-open", str(path)], check=False)

        except Exception:
            messagebox.showerror(
                self._t("download_failed_title"),
                f"{self._t('open_folder_error')} {path}",
            )

    def run(self):
        self.url_entry.focus()
        self.window.mainloop()