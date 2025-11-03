import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
ASSETS_DIR = BASE_DIR / "assets"
VIDEOS_DIR = ASSETS_DIR / "videos"
PHOTOS_DIR = BASE_DIR / "gallery"
COUNTER_FILE = BASE_DIR / "counter.txt"

PHOTOS_DIR.mkdir(exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

def initialize_counter():
    """
    Initializes the photo counter file (counter.txt) if it doesn't exist.

    This file acts as a persistent memory to track the number of photos
    taken, ensuring that each new photo has a unique ID (e.g., 001, 002)
    even after the application is closed and restarted.
    """
    if not COUNTER_FILE.exists():
        COUNTER_FILE.write_text("0")

def get_next_id():
    """
    Get next photo ID and increment counter
    Returns: string like "001", "002", etc.
    """
    initialize_counter()
    current = int (COUNTER_FILE.read_text().strip())
    current += 1
    COUNTER_FILE.write_text(str(current))

    return f"{current:03d}"

class MirrorSettings:
    """Global settings for the magic mirror"""
    selected_camera = 0
    available_cameras = []

    orientation = "vertical"

    HORIZONTAL_SIZE = (1920, 1080)
    VERTICAL_SIZE = (1080, 1920)
    ADMIN_SIZE = (800, 600)

    @classmethod
    def get_window_size(cls):
        """Returns current window size based on orientation"""
        if cls.orientation == "vertical":
            return cls.VERTICAL_SIZE
        return cls.HORIZONTAL_SIZE

initialize_counter()

START_VIDEO_PATH = str(VIDEOS_DIR / "start_loop.mp4")

if __name__ == "__main__":
    print(f"Base directory: {BASE_DIR}")
    print(f"Photos will be saved to: {PHOTOS_DIR}")
    print(f"Next photo ID: {get_next_id()}")
    print(f"Window size: {MirrorSettings.get_window_size()}")










