from pathlib import Path

from PIL import Image, ImageOps


def normalize_image(input_path: str, output_path: str) -> str:
    """
    Prepare an uploaded image for further processing.

    The original image is not modified.

    Operations:
    - Correct EXIF orientation
    - Preserve grayscale images
    - Convert normal images to RGB
    - Save the processed image as PNG
    """

    input_path = Path(input_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with Image.open(input_path) as image:

        image = ImageOps.exif_transpose(image)

        if image.mode in ("L", "I", "I;16"):
            processed_image = image.copy()
        else:
            processed_image = image.convert("RGB")

        processed_image.save(
            output_path,
            format="PNG"
        )

    return str(output_path)


def resize_if_needed(
    input_path: str,
    output_path: str,
    max_width: int = 4096,
    max_height: int = 4096,
) -> str:
    """
    Resize very large images while maintaining aspect ratio.
    """

    input_path = Path(input_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with Image.open(input_path) as image:

        image.thumbnail(
            (max_width, max_height),
            Image.Resampling.LANCZOS
        )

        image.save(
            output_path,
            format="PNG"
        )

    return str(output_path)