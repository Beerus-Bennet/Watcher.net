"""Lokale Weboberflaeche von Watcher.net.

Start: python app.py          -> nur auf diesem Computer
       python app.py --handy  -> auch fuer Handys im selben WLAN erreichbar
Die Windows-App (Watcher.exe) startet genau diese Datei.
"""
import os
import socket
import sys
import threading
import webbrowser

from flask import Flask, jsonify, render_template, request, send_file

from downloader import DownloadError, download

# In der fertigen App liegen templates/ und static/ im entpackten Ordner
BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder=os.path.join(BASE, "templates"),
            static_folder=os.path.join(BASE, "static"))
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


def _free_port(preferred: int = 5000) -> int:
    for port in [preferred, *range(5001, 5050)]:
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return preferred


def main() -> None:
    handy = "--handy" in sys.argv
    host = "0.0.0.0" if handy else "127.0.0.1"
    port = _free_port()
    url = f"http://127.0.0.1:{port}"
    print("=" * 52)
    print("  Watcher.net laeuft.")
    print(f"  Falls sich kein Browser oeffnet: {url}")
    if handy:
        print(f"  Auf dem Handy (gleiches WLAN): http://{_lan_ip()}:{port}")
    print("  Zum Beenden dieses Fenster schliessen.")
    print("=" * 52)
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
