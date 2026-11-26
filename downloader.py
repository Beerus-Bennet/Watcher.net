"""Kernlogik: Link rein, MP3 oder MP4 in bester verfuegbarer Qualitaet raus.

Nutzt yt-dlp (unterstuetzt YouTube, Instagram, TikTok und viele mehr)
und ffmpeg zum Zusammenfuegen und Umwandeln.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp

# Dienste mit Kopierschutz (DRM). Diese werden bewusst nicht unterstuetzt.
BLOCKED_HOSTS = ("netflix.com", "disneyplus.com", "primevideo.com", "amazon.", "spotify.com")

AAC_ARGS = ["-c:v", "copy", "-c:a", "aac", "-b:a", "256k"]

DEFAULT_OUT = Path.home() / "Downloads" / "Watcher.net"


class DownloadError(Exception):
    pass


def check_url(url: str) -> str:
    url = url.strip()
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise DownloadError("Das sieht nicht nach einem gueltigen Link aus.")
    host = parsed.netloc.lower()
    if any(b in host for b in BLOCKED_HOSTS):
        raise DownloadError(
            "Dieser Dienst ist kopiergeschuetzt (DRM) und wird nicht unterstuetzt."
        )
    return url


def _options(fmt: str, out_dir: Path) -> dict:
    opts = {
        "outtmpl": str(out_dir / "%(title).150B [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "noprogress": True,
        "no_warnings": True,
        "restrictfilenames": False,
        "windowsfilenames": True,
    }
    if fmt == "mp3":
        opts.update(
            format="bestaudio/best",
            postprocessors=[
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",  # beste VBR-Qualitaet (~245 kbit/s)
                },
                {"key": "FFmpegMetadata"},
                {"key": "EmbedThumbnail"},
            ],
            writethumbnail=True,
        )
    elif fmt == "mp4":
        opts.update(
            # Bestes Video + bestes Audio, sonst bestes kombiniertes Format
            format="bv*+ba/b",
            merge_output_format="mp4",
            # Audio als AAC, damit die MP4 ueberall abspielbar ist (Video bleibt unveraendert)
            postprocessor_args={
                "merger": AAC_ARGS,
                "videoremuxer": AAC_ARGS,
            },
            postprocessors=[
                # Falls nur eine einzelne Datei (z.B. .webm) kam: in MP4 umpacken
                {"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"},
                {"key": "FFmpegMetadata"},
            ],
        )
    else:
        raise DownloadError("Format muss 'mp3' oder 'mp4' sein.")
    return opts


def download(url: str, fmt: str = "mp4", out_dir: Path | str = DEFAULT_OUT) -> Path:
    """Laedt den Link herunter und gibt den Pfad der fertigen Datei zurueck."""
    if shutil.which("ffmpeg") is None:
        raise DownloadError("ffmpeg wurde nicht gefunden. Bitte installieren (siehe README).")
    url = check_url(url)
    fmt = fmt.lower()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(_options(fmt, out_dir)) as ydl:
            info = ydl.extract_info(url, download=True)
            if info.get("_type") == "playlist" and info.get("entries"):
                info = info["entries"][0]
            downloads = info.get("requested_downloads") or [{}]
            final = downloads[0].get("filepath") or ydl.prepare_filename(info)
            path = Path(final).with_suffix("." + fmt)
    except yt_dlp.utils.DownloadError as e:
        msg = str(e).replace("ERROR: ", "")
        if "DRM" in msg:
            msg = "Dieses Video ist kopiergeschuetzt (DRM) und kann nicht geladen werden."
        raise DownloadError(msg) from e

    if not path.exists():
        raise DownloadError("Download fertig, aber die Datei wurde nicht gefunden.")
    return path
