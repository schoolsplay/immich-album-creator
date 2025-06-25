# 📂 Immich Album Creator

A simple Python 3 script to automatically create albums in [Immich](https://github.com/immich-app/immich) from a directory structure on your local filesystem.

Each subdirectory under a specified root folder becomes a new album, containing all media assets (images/videos) found in that folder via Immich's `/api/view/folder` endpoint.

---

## ✨ Features

- ⚠️ **Note:** This script does *not* scan subdirectories recursively. Only immediate subfolders of `LIBRARY_ROOT` are processed.

- Scans all subdirectories of a given root path
- Automatically queries Immich for existing media in each folder
- Creates a new album (if it doesn’t already exist)
- Skips empty folders and existing albums
- Supports `--dry-run` mode to preview actions without making changes
- Uses the Immich HTTP API with `x-api-key` authentication

---

## 🚀 Usage

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
API_KEY = "your-api-key"           # Immich API key
```

---

## 📌 Requirements

- Python 3.6+
- `requests` library (`pip install requests`)
- An active Immich instance with API access enabled

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.
