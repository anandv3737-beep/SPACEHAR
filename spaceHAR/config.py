from pathlib import Path


# ==============================
# PROJECT PATHS
# ==============================

BASE_DIR = Path(__file__).resolve().parent

RECORDINGS_DIR = BASE_DIR / "recordings"
LOGS_DIR = BASE_DIR / "logs"

RECORDINGS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


# ==============================
# CAMERA SETTINGS
# ==============================

CAMERA_INDEX = 0

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_FPS = 20


# ==============================
# AI / YOLO SETTINGS
# ==============================

YOLO_MODEL = "yolo11n.pt"

DETECTION_CONFIDENCE = 0.50

PERSON_CLASS_ID = 0


# ==============================
# ACTIVITY RECOGNITION
# ==============================

ACTIVITY_WINDOW = 15

MIN_ACTIVITY_FRAMES = 5

DUPLICATE_EVENT_COOLDOWN = 2.0


# ==============================
# VIDEO SETTINGS
# ==============================

JPEG_QUALITY = 80

RECORDING_CODEC = "mp4v"


# ==============================
# SERVER SETTINGS
# ==============================

HOST = "0.0.0.0"

PORT = 5000

DEBUG = False