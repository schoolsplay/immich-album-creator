import fnmatch
import os
import requests
import argparse
import logging
import logging.handlers

# Configuration constants from creds
from creds import IMMICH_HOST, LIBRARY_ROOT, API_KEY, EXCLUSION_PATTERNS


# Authentication headers
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# Configure logging, a console and rotating file handler
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('create-album')

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Rotating file handler
file_handler = logging.handlers.RotatingFileHandler('create-album.log', maxBytes=1024 * 500, backupCount=2)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

logger.info("Start logging process")

def get_folder_assets(abs_folder_path: str):
    """Retrieve asset IDs from a folder using its absolute path."""
    url = f"http://{IMMICH_HOST}/api/view/folder"
    params = {"path": abs_folder_path}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        asset_ids = [item["id"] for item in data]
        return asset_ids
    except requests.RequestException as e:
        logger.error(f"Failed to get assets for '{abs_folder_path}': {e}")
        return []


def album_exists(album_name: str):
    """Check if an album with the given name already exists."""
    url = f"http://{IMMICH_HOST}/api/albums"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        albums = response.json()
        return any(album.get("albumName") == album_name for album in albums)
    except requests.RequestException as e:
        logger.error(f"Failed to check existing albums: {e}")
        return False


def create_album(album_name: str, asset_ids: list, dry_run: bool):
    """Create an album if it does not already exist."""
    if album_exists(album_name):
        logger.info(f"Album '{album_name}' already exists.")
        return

    if dry_run:
        logger.debug(f"[DRY-RUN] Simulated creation of album '{album_name}' with {len(asset_ids)} assets.")
        return

    url = f"http://{IMMICH_HOST}/api/albums"
    payload = {
        "albumName": album_name,
        "assetIds": asset_ids,
        "description": ""
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        logger.debug(f"Album created: {album_name} ({len(asset_ids)} assets)")
    except requests.RequestException as e:
        logger.error(f"Failed to create album '{album_name}': {e}")


def main(dry_run: bool):
    logger.info(f"Scanning for directories in '{LIBRARY_ROOT}'...")
    all_subdirs = [entry for entry in os.scandir(LIBRARY_ROOT) if entry.is_dir()]
    subdirs = [
        entry for entry in all_subdirs
        if not any(fnmatch.fnmatch(entry.name, pattern) for pattern in EXCLUSION_PATTERNS)
    ]
    excluded_count = len(all_subdirs) - len(subdirs)
    if excluded_count > 0:
        logger.info(f"Found {len(all_subdirs)} total directories. Excluding {excluded_count} based on patterns.")
    total = len(subdirs)

    for idx, entry in enumerate(subdirs, start=1):
        abs_path = entry.path
        folder_name = entry.name
        logger.debug(f"\n[{idx}/{total}] Processing folder: {abs_path}")

        asset_ids = get_folder_assets(abs_path)
        if not asset_ids:
            logger.warning(f"No assets found in '{abs_path}'")
            continue

        create_album(folder_name, asset_ids, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Immich albums from local subdirectories.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without creating albums")
    args = parser.parse_args()

    main(dry_run=args.dry_run)
