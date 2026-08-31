from datetime import datetime
from pathlib import Path

from PIL import Image


def extract_metadata(file_path: str) -> dict:
    """
    Extract useful metadata from an uploaded image.
    """

    file_path = Path(file_path)

    metadata = {
        "filename": file_path.name,
        "file_size_bytes": file_path.stat().st_size,
        "created_at": datetime.now().isoformat(),
    }

    try:

        with Image.open(file_path) as image:

            metadata.update({
                "format": image.format,
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
            })

            exif_data = image.getexif()

            if exif_data:

                metadata["exif"] = {
                    str(key): str(value)
                    for key, value in exif_data.items()
                }

    except Exception as exc:

        metadata["metadata_error"] = str(exc)

    return metadata