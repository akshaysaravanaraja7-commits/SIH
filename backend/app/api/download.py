from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.services.storage_service import storage_service


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Download"]
)


# --------------------------------------------------
# Download enhanced image
# --------------------------------------------------

@router.get(
    "/download/{image_id}"
)
async def download_enhanced_image(
    image_id: str
):
    """
    Download the enhanced image associated
    with the given image ID.
    """

    # --------------------------------------------------
    # Find enhanced image
    # --------------------------------------------------

    output_path = storage_service.find_output(
        image_id
    )

    if output_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Enhanced image not found. "
                "Please process the image first."
            )
        )

    # --------------------------------------------------
    # Determine media type
    # --------------------------------------------------

    extension = output_path.suffix.lower()

    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".tif": "image/tiff",
        ".tiff": "image/tiff",
    }

    media_type = media_types.get(
        extension,
        "application/octet-stream"
    )

    # --------------------------------------------------
    # Return downloadable file
    # --------------------------------------------------

    return FileResponse(
        path=output_path,
        media_type=media_type,
        filename=(
            f"{image_id}_enhanced{extension}"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; '
                f'filename="{image_id}_enhanced{extension}"'
            )
        }
    )