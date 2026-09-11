from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"


# --------------------------------------------------
# File configuration
# --------------------------------------------------

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/tiff",
    "image/webp",
}


# --------------------------------------------------
# Application configuration
# --------------------------------------------------

APP_NAME = "Lunar PSR Image Enhancement API"
APP_VERSION = "1.0.0"


# --------------------------------------------------
# Processing configuration
# --------------------------------------------------

DEFAULT_OUTPUT_FORMAT = "png"