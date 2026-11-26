# Watcher.net

<img src="static/icons/icon-512-rounded.png" alt="Watcher.net Icon" width="128">

Link von YouTube, Instagram Reels oder TikTok einfügen und als **MP3** (Audio) oder **MP4** (Video) in der besten verfügbaren Qualität speichern. Läuft lokal auf deinem Rechner, mit einer kleinen Oberfläche im Browser.

> Nur für den privaten Gebrauch und nur für Inhalte, an denen du die Rechte hast oder deren Download erlaubt ist. Kopiergeschützte Dienste wie Netflix, Disney+ oder Spotify werden bewusst nicht unterstützt.

## Voraussetzungen

- **Python 3.10 oder neuer**: https://www.python.org/downloads/ (unter Windows beim Installieren „Add Python to PATH“ anhaken)
- **ffmpeg** (zum Zusammenfügen und Umwandeln):
  - Windows: `winget install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

## Starten

- **Windows:** Doppelklick auf `start.bat`
- **macOS/Linux:** `./start.sh`

Beim ersten Start werden die Pakete installiert. Danach öffnet sich der Browser auf http://127.0.0.1:5000. Link einfügen, MP3 oder MP4 wählen, fertig.

Die Dateien landen in `Downloads/Watcher.net`.

## Auf dem Handy nutzen

1. Auf dem Computer mit `start.bat --handy` (Windows) bzw. `./start.sh --handy` (Mac/Linux) starten.
2. Im Fenster steht eine Adresse wie `http://192.168.0.23:5000`. Diese auf dem Handy öffnen (gleiches WLAN).
3. **iPhone:** Teilen → „Zum Home-Bildschirm“. **Android:** Menü (⋮) → „Zum Startbildschirm hinzufügen“.

Watcher.net erscheint dann mit eigenem Icon wie eine App. Heruntergeladene Dateien kannst du über „Datei öffnen“ direkt aufs Handy laden. Der Computer muss dafür laufen.

> Mit `--handy` ist die Seite für alle Geräte im WLAN erreichbar. Nur im eigenen Heimnetz verwenden.

## Kommandozeile (optional)

```bash
python cli.py "https://www.youtube.com/watch?v=..." mp3
python cli.py "https://www.tiktok.com/@user/video/..." mp4 -o ./meine-videos
```

## Was „beste Qualität“ heißt

- **MP4:** bestes Video plus beste Tonspur, zusammengefügt. Das Video wird nicht neu kodiert. Die Tonspur wird in AAC umgewandelt, damit die Datei auf jedem Gerät abspielt.
- **MP3:** beste Tonspur, umgewandelt in MP3 mit höchster Qualitätsstufe (VBR V0), mit Titel und Vorschaubild. Hinweis: Die Originalspur ist meist Opus oder AAC, MP3 ist also immer eine Umwandlung.

## Wenn etwas nicht klappt

Plattformen ändern sich oft. Die Startskripte aktualisieren `yt-dlp` bei jedem Start automatisch, das behebt die meisten Fehler. Private Videos und manche Instagram-Inhalte brauchen einen Login und funktionieren derzeit nicht.

## Icons

Alle Größen liegen in `static/icons/` (Quelle: `icon.svg`):

| Datei | Größe | Wofür |
|---|---|---|
| `favicon.ico` | 16, 32, 48 | Browser-Tab |
| `apple-touch-icon.png` | 180×180 | iPhone/iPad Home-Bildschirm |
| `icon-192.png`, `icon-512.png` | 192, 512 | Android / installierte Web-App |
| `icon-maskable-192.png`, `icon-maskable-512.png` | 192, 512 | Android (runde/abgerundete Formen) |
| `icon-512-rounded.png` | 512 | README, Vorschau |

## Herunterladen

Oben auf GitHub auf **Code → Download ZIP** klicken, entpacken, dann wie unter „Starten“ beschrieben loslegen. Mit Git: `git clone https://github.com/Beerus-Bennet/watcher.net.git`

## Lizenz

MIT, siehe [LICENSE](LICENSE).
