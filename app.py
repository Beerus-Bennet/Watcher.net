"""Lokale Weboberflaeche von Watcher.net.

Start: python app.py          -> nur auf diesem Computer (http://127.0.0.1:5000)
       python app.py --handy  -> auch fuer Handys im selben WLAN erreichbar
"""
import socket
import sys
import threading
import webbrowser

from flask import Flask, jsonify, render_template, request, send_file

from downloader import DownloadError, download

app = Flask(__name__)
_files: dict[str, str] = {}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/download")
def api_download():
    data = request.get_json(silent=True) or {}
    try:
        path = download(data.get("url", ""), data.get("format", "mp4"))
    except DownloadError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:  # unerwartete Fehler lesbar zurueckgeben
        return jsonify(error=f"Unerwarteter Fehler: {e}"), 500
    key = str(len(_files))
    _files[key] = str(path)
    return jsonify(name=path.name, folder=str(path.parent), file=f"/file/{key}")


@app.get("/file/<key>")
def get_file(key):
    path = _files.get(key)
    if not path:
        return "Nicht gefunden", 404
    return send_file(path, as_attachment=True)


def _lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    handy = "--handy" in sys.argv
    host = "0.0.0.0" if handy else "127.0.0.1"
    if handy:
        print(f"\nAuf dem Handy (gleiches WLAN) oeffnen: http://{_lan_ip()}:5000\n")
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(host=host, port=5000)
