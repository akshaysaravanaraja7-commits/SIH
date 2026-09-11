from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.config import ALLOWED_IMAGE_TYPES
from app.models.schemas import UploadResponse
from app.services.image_service import image_service
from app.services.job_service import job_service


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Upload"]
)


# --------------------------------------------------
# Upload image
# --------------------------------------------------

@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_image(
    image: UploadFile = File(...)
):
    """
    Upload a lunar image for processing.
    """

    # --------------------------------------------------
    # Validate filename
    # --------------------------------------------------

    if not image.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided."
        )

    # --------------------------------------------------
    # Validate content type
    # --------------------------------------------------

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported image format. "
                "Supported formats: PNG, JPEG, TIFF, WEBP."
            )
        )

    # --------------------------------------------------
    # Save image
    # --------------------------------------------------

    try:
        result = await image_service.save_uploaded_image(
            image
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except Exception as error:
        print(f"Upload error: {error}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded image."
        )

    # --------------------------------------------------
    # Create processing job
    # --------------------------------------------------

    job_service.create_job(
        image_id=result["image_id"],
        filename=result["filename"]
    )

    # --------------------------------------------------
    # Return response
    # --------------------------------------------------

    return UploadResponse(
        image_id=result["image_id"],
        filename=result["filename"],
        status="uploaded",
        message="Image uploaded successfully."
    )