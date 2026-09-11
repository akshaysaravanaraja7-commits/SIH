from fastapi import APIRouter, HTTPException, status

from app.models.schemas import EnhancementResponse
from app.services.image_service import image_service
from app.services.enhancement_service import enhancement_service
from app.services.job_service import job_service
from app.utils.file_utils import get_output_path


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Enhancement"]
)


# --------------------------------------------------
# Enhance image
# --------------------------------------------------

@router.post(
    "/enhance/{image_id}",
    response_model=EnhancementResponse
)
async def enhance_image(
    image_id: str
):
    """
    Enhance an uploaded lunar image.

    The image must already exist in the uploads directory.
    """

    # --------------------------------------------------
    # Find uploaded image
    # --------------------------------------------------

    input_path = image_service.get_image_path(
        image_id
    )

    if input_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found."
        )

    # --------------------------------------------------
    # Mark job as processing
    # --------------------------------------------------

    job_service.update_job(
        image_id=image_id,
        status="processing",
        progress=10,
        message="Image enhancement started."
    )

    # --------------------------------------------------
    # Define output path
    # --------------------------------------------------

    output_path = get_output_path(
        image_id,
        ".png"
    )

    # --------------------------------------------------
    # Run enhancement
    # --------------------------------------------------

    try:
        result = enhancement_service.enhance(
            input_path=input_path,
            output_path=output_path
        )

        # --------------------------------------------------
        # Mark job as completed
        # --------------------------------------------------

        job_service.update_job(
            image_id=image_id,
            status="completed",
            progress=100,
            message="Image enhancement completed."
        )

    except FileNotFoundError as error:

        job_service.update_job(
            image_id=image_id,
            status="failed",
            progress=0,
            message="Input image was not found."
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except ValueError as error:

        job_service.update_job(
            image_id=image_id,
            status="failed",
            progress=0,
            message="Invalid image."
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except Exception as error:

        print(f"Enhancement error: {error}")

        job_service.update_job(
            image_id=image_id,
            status="failed",
            progress=0,
            message="Image enhancement failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image enhancement failed."
        )

    # --------------------------------------------------
    # Return response
    # --------------------------------------------------

    return EnhancementResponse(
        image_id=image_id,
        status=result["status"],
        message=(
            "Image enhanced successfully. "
            f"Processing time: "
            f"{result['processing_time']} seconds."
        )
    )