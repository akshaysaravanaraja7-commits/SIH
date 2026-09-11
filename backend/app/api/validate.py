from fastapi import APIRouter, HTTPException, status

from app.services.image_service import image_service
from app.services.job_service import job_service
from app.image_handler.validator import (
    validate_extension,
    validate_file_size,
    validate_image_content,
)


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Validation"],
)


# --------------------------------------------------
# Validate uploaded image
# --------------------------------------------------

@router.post(
    "/validate/{image_id}"
)
async def validate_image(
    image_id: str
):
    """
    Validate an uploaded lunar image.

    Uses Member 2's image validation module for:
    - File extension validation
    - File size validation
    - Actual image content validation
    """

    # --------------------------------------------------
    # Find image
    # --------------------------------------------------

    image_path = image_service.get_image_path(
        image_id
    )

    if image_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found.",
        )

    # --------------------------------------------------
    # Mark validation started
    # --------------------------------------------------

    job_service.update_job(
        image_id=image_id,
        status="validating",
        progress=20,
        message="Image validation started.",
    )

    try:
        # --------------------------------------------------
        # Validate file extension
        # --------------------------------------------------

        if not validate_extension(
            image_path.name
        ):
            job_service.update_job(
                image_id=image_id,
                status="failed",
                progress=0,
                message="Unsupported image format.",
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Unsupported image format. "
                    "Allowed formats: JPG, JPEG, PNG, TIFF."
                ),
            )

        # --------------------------------------------------
        # Validate file size
        # --------------------------------------------------

        file_size = image_path.stat().st_size

        if not validate_file_size(file_size):
            job_service.update_job(
                image_id=image_id,
                status="failed",
                progress=0,
                message="Image exceeds the allowed file size.",
            )

            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image exceeds the 50 MB size limit.",
            )

        if file_size == 0:
            job_service.update_job(
                image_id=image_id,
                status="failed",
                progress=0,
                message="Image file is empty.",
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file is empty.",
            )

        # --------------------------------------------------
        # Validate actual image content
        # --------------------------------------------------

        valid, message = validate_image_content(
            str(image_path)
        )

        if not valid:
            job_service.update_job(
                image_id=image_id,
                status="failed",
                progress=0,
                message="Invalid or corrupted image.",
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message,
            )

        # --------------------------------------------------
        # Validation successful
        # --------------------------------------------------

        job_service.update_job(
            image_id=image_id,
            status="uploaded",
            progress=30,
            message="Image validation completed.",
        )

        return {
            "image_id": image_id,
            "status": "valid",
            "message": "Image passed validation.",
            "file_size_bytes": file_size,
        }

    except HTTPException:
        raise

    except Exception as error:

        print(f"Validation error: {error}")

        job_service.update_job(
            image_id=image_id,
            status="failed",
            progress=0,
            message="Image validation failed.",
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image validation failed.",
        )