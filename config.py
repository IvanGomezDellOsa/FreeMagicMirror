from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
ASSETS_DIR = BASE_DIR / "assets"
VIDEOS_DIR = ASSETS_DIR / "videos"
PHOTOS_DIR = BASE_DIR / "gallery"
COUNTER_FILE = BASE_DIR / "counter.txt"

PHOTOS_DIR.mkdir(exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def initialize_counter():
    """Create counter.txt if missing, starting from 0."""
    if not COUNTER_FILE.exists():
        COUNTER_FILE.write_text("0")


def get_next_id():
    """Return the next photo ID (e.g., '001') and update the counter."""
    initialize_counter()
    current = int(COUNTER_FILE.read_text().strip())
    current += 1
    COUNTER_FILE.write_text(str(current))
    return f"{current:03d}"


class MirrorSettings:
    """Holds global configuration values for FreeMagicMirror."""

    selected_camera = 0
    available_cameras = []
    selected_screen = 0
    orientation = "vertical"

    HORIZONTAL_SIZE = (1920, 1080)
    VERTICAL_SIZE = (1080, 1920)
    ADMIN_SIZE = (800, 600)

    @classmethod
    def get_window_size(cls):
        """Return window size according to current orientation."""
        if cls.orientation == "vertical":
            return cls.VERTICAL_SIZE
        return cls.HORIZONTAL_SIZE


initialize_counter()

START_VIDEO_PATH = str(VIDEOS_DIR / "start_loop.mp4")
POSE_VIDEO_PATH = str(VIDEOS_DIR / "pose_prompt.mp4")

if __name__ == "__main__":
    print(f"Base directory: {BASE_DIR}")
    print(f"Photos will be saved to: {PHOTOS_DIR}")
    print(f"Next photo ID: {get_next_id()}")
    print(f"Window size: {MirrorSettings.get_window_size()}")