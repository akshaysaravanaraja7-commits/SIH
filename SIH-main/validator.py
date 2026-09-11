from pathlib import Path

from PIL import Image


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_extension(filename: str) -> bool:
    """
    Check whether the uploaded file has a supported image extension.
    """

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


def validate_file_size(file_size: int) -> bool:
    """
    Check whether the uploaded file is within the allowed size limit.
    """

    return file_size <= MAX_FILE_SIZE


def validate_image_content(file_path: str) -> tuple[bool, str]:
    """
    Check whether the file is a valid and readable image.
    """

    try:
        with Image.open(file_path) as image:
            image.verify()

        return True, "Valid image"

    except Exception as exc:
        return False, f"Invalid or corrupted image: {exc}"


def get_image_info(file_path: str) -> dict:
    """
    Get basic information about an image.
    """

    try:
        with Image.open(file_path) as image:

            return {
                "format": image.format,
                "mode": image.mode,
                "width": image.width,
                "height": image.height,
            }

    except Exception as exc:

        return {
            "error": str(exc)
        }