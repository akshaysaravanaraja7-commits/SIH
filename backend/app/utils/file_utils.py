from pathlib import Path
from uuid import uuid4

from app.config import (
    OUTPUT_DIR,
    UPLOAD_DIR,
)


# --------------------------------------------------
# Ensure directories exist
# --------------------------------------------------

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Generate unique image ID
# --------------------------------------------------

def generate_image_id() -> str:
    """
    Generate a unique identifier for an uploaded image.
    """

    return uuid4().hex


# --------------------------------------------------
# Get file extension
# --------------------------------------------------

def get_file_extension(
    filename: str
) -> str:
    """
    Extract the file extension from a filename.

    Example:
        lunar_image.png -> .png
    """

    extension = Path(
        filename
    ).suffix.lower()

    if not extension:
        return ""

    return extension


# --------------------------------------------------
# Create stored filename
# --------------------------------------------------

def create_stored_filename(
    image_id: str,
    original_filename: str
) -> str:
    """
    Create a safe server-side filename.
    """

    extension = get_file_extension(
        original_filename
    )

    return f"{image_id}{extension}"


# --------------------------------------------------
# Get upload path
# --------------------------------------------------

def get_upload_path(
    image_id: str,
    original_filename: str
) -> Path:
    """
    Return the complete path for an uploaded image.
    """

    filename = create_stored_filename(
        image_id,
        original_filename
    )

    return UPLOAD_DIR / filename


# --------------------------------------------------
# Get output path
# --------------------------------------------------

def get_output_path(
    image_id: str,
    extension: str = ".png"
) -> Path:
    """
    Return the complete path for an enhanced image.
    """

    extension = extension.lower()

    if not extension.startswith("."):
        extension = f".{extension}"

    filename = (
        f"{image_id}_enhanced{extension}"
    )

    return OUTPUT_DIR / filename