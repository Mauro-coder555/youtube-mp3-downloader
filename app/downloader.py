from pathlib import Path
from yt_dlp import YoutubeDL


class DownloadError(Exception):
    """Custom exception for download errors."""
    pass


def get_user_downloads_folder() -> Path:
    """
    Returns the default Downloads folder for the current user.
    Works well for Windows and also keeps the app usable on other systems.
    """
    downloads_path = Path.home() / "Downloads"

    if downloads_path.exists():
        return downloads_path

    return Path.home()


def download_youtube_audio_as_mp3(url: str, output_dir: Path | None = None) -> Path:
    """
    Downloads audio from a YouTube URL and converts it to MP3.

    Args:
        url: YouTube video URL.
        output_dir: Folder where the MP3 file will be saved.

    Returns:
        Path to the folder where the MP3 was saved.

    Raises:
        DownloadError: If the URL is empty or the download fails.
    """
    if not url or not url.strip():
        raise DownloadError("Please enter a valid YouTube URL.")

    downloads_path = output_dir or get_user_downloads_folder()
    downloads_path.mkdir(parents=True, exist_ok=True)

    ydl_options = {
        "format": "bestaudio/best",
        "outtmpl": str(downloads_path / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with YoutubeDL(ydl_options) as ydl:
            ydl.download([url])

        return downloads_path

    except Exception as error:
        raise DownloadError(
            "The download failed. Please check the URL, your internet connection, "
            "and make sure FFmpeg is installed."
        ) from error