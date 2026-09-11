from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.utils.file_utils import OUTPUT_DIR


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Result"]
)


# --------------------------------------------------
# Get enhanced image
# --------------------------------------------------

@router.get(
    "/result/{image_id}"
)
async def get_enhanced_image(
    image_id: str
):
    """
    Return the enhanced image associated with image_id.
    """

    # --------------------------------------------------
    # Find enhanced output
    # --------------------------------------------------

    enhanced_files = list(
        OUTPUT_DIR.glob(
            f"{image_id}_enhanced.*"
        )
    )

    # --------------------------------------------------
    # Result not available
    # --------------------------------------------------

    if not enhanced_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enhanced image not found. "
                   "Please process the image first."
        )

    output_path = enhanced_files[0]

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
    # Return image
    # --------------------------------------------------

    return FileResponse(
        path=output_path,
        media_type=media_type,
        filename=f"{image_id}_enhanced{extension}"
    )