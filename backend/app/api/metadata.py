from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from app.services.image_service import image_service
from app.services.job_service import job_service


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Metadata"]
)


# --------------------------------------------------
# Get image metadata
# --------------------------------------------------

@router.get(
    "/metadata/{image_id}"
)
async def get_image_metadata(
    image_id: str
):
    """
    Return basic metadata for an uploaded image.
    """

    # --------------------------------------------------
    # Find uploaded image
    # --------------------------------------------------

    image_path = image_service.get_image_path(
        image_id
    )

    if image_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found."
        )

    # --------------------------------------------------
    # Get job information
    # --------------------------------------------------

    job = job_service.get_job(
        image_id
    )

    # --------------------------------------------------
    # Get file information
    # --------------------------------------------------

    file_size = image_path.stat().st_size

    extension = image_path.suffix.lower()

    # --------------------------------------------------
    # Return metadata
    # --------------------------------------------------

    return {
        "image_id": image_id,
        "filename": (
            job["filename"]
            if job
            else image_path.name
        ),
        "format": extension.replace(".", "").upper(),
        "file_size_bytes": file_size,
        "status": (
            job["status"]
            if job
            else "uploaded"
        ),
        "progress": (
            job["progress"]
            if job
            else 0
        ),
        "created_at": (
            job["created_at"]
            if job
            else None
        ),
        "updated_at": (
            job["updated_at"]
            if job
            else None
        ),
    }