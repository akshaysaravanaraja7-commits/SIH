from fastapi import APIRouter, HTTPException, status

from app.models.schemas import StatusResponse
from app.services.image_service import image_service
from app.services.job_service import job_service


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Status"]
)


# --------------------------------------------------
# Get image processing status
# --------------------------------------------------

@router.get(
    "/status/{image_id}",
    response_model=StatusResponse
)
async def get_image_status(
    image_id: str
):
    """
    Return the current processing status of an image.
    """

    # --------------------------------------------------
    # Get job
    # --------------------------------------------------

    job = job_service.get_job(
        image_id
    )

    if job is None:

        # Fallback: check whether the image exists
        if not image_service.image_exists(image_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found."
            )

        return StatusResponse(
            image_id=image_id,
            status="uploaded",
            progress=0,
            message="Image uploaded."
        )

    # --------------------------------------------------
    # Return current state
    # --------------------------------------------------

    return StatusResponse(
        image_id=job["image_id"],
        status=job["status"],
        progress=job["progress"],
        message=job["message"]
    )