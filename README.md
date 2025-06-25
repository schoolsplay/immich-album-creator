# 📂 Immich Album Creator

A simple Python 3 script to automatically create albums in [Immich](https://github.com/immich-app/immich) from a directory structure on your local filesystem.

Each subdirectory under a specified root folder becomes a new album, containing all media assets (images/videos) found in that folder.

The script uses Immich's HTTP API to retrieve asset metadata and create albums.

---

## ✨ Features

- ⚠️ **Note:** For now this script does *not* scan subdirectories recursively. Only immediate subfolders of `LIBRARY_ROOT` are processed.

- Scans all subdirectories of a given root path
- Automatically queries Immich for existing media in each folder
- Creates a new album (if it doesn’t already exist)
- Skips empty folders and existing albums
- Supports `--dry-run` mode to preview actions without making changes
- Uses the Immich HTTP API with `x-api-key` authentication

---

## 🚀 Usage

⚠️ **Important:** Before running the script, make sure you have triggered a rescan of your external library in Immich (via the web UI or API). This ensures all media files are indexed and available via the `/api/view/folder` endpoint.

🔑 Note: You must create an API key in Immich (from your user settings) and set it in the script as the API_KEY value. This key is required to authenticate API requests.

```bash
python3 create-album.py
```

To simulate actions without creating albums:

```bash
python3 create-album.py --dry-run
```

---

## 🔧 Configuration

Edit the constants at the top of the script to match your environment:

```python
IMMICH_HOST = "192.168.1.10:3001"   # Immich server IP and port
LIBRARY_ROOT = "/mnt/SSD/FOTO"     # Root path to scan
API_KEY = "LVonX8XvAI85EST9Ryh3fPpoUliQkSHjeRDs9Hx9I" # Immich API key
```

---

## 📌 Requirements

- Python 3.6+
- `requests` library (`pip install requests`)
- An active Immich instance with API access enabled

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.
