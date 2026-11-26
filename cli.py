"""Kommandozeile: python cli.py <link> [mp3|mp4] [-o ordner]"""
import argparse
import sys

from downloader import DEFAULT_OUT, DownloadError, download


def main() -> int:
    p = argparse.ArgumentParser(description="Link zu MP3/MP4 in bester Qualitaet")
    p.add_argument("url", help="YouTube-, Instagram- oder TikTok-Link")
    p.add_argument("format", nargs="?", default="mp4", choices=["mp3", "mp4"])
    p.add_argument("-o", "--out", default=str(DEFAULT_OUT), help="Zielordner")
    a = p.parse_args()
    try:
        print("Lade herunter ...")
        path = download(a.url, a.format, a.out)
    except DownloadError as e:
        print(f"Fehler: {e}", file=sys.stderr)
        return 1
    print(f"Fertig: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
