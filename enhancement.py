import os
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from image_handler.metadata import extract_metadata
from image_handler.preprocessor import normalize_image
from image_handler.validator import (
    validate_extension,
    validate_file_size,
    validate_image_content,
)


router = APIRouter(
    prefix="/api",
    tags=["Image Handling"],
)


UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

MAX_FILE_SIZE = 50 * 1024 * 1024


os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload, validate, preprocess, and store an image.
    """

    # ----------------------------------------
    # 1. Check filename
    # ----------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    # ----------------------------------------
    # 2. Check file extension
    # ----------------------------------------

    if not validate_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Allowed formats: JPG, JPEG, PNG, TIFF."
            ),
        )

    # ----------------------------------------
    # 3. Generate unique image ID
    # ----------------------------------------

    image_id = str(uuid.uuid4())

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    original_filename = (
        f"{image_id}{extension}"
    )

    upload_path = os.path.join(
        UPLOAD_DIR,
        original_filename,
    )

    # ----------------------------------------
    # 4. Save uploaded file with size limit
    # ----------------------------------------

    total_size = 0

    try:

        with open(upload_path, "wb") as buffer:

            while True:

                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:

                    buffer.close()

                    if os.path.exists(upload_path):
                        os.remove(upload_path)

                    raise HTTPException(
                        status_code=413,
                        detail="Image exceeds the 50 MB size limit.",
                    )

                buffer.write(chunk)

    except HTTPException:
        raise

    except Exception as exc:

        if os.path.exists(upload_path):
            os.remove(upload_path)

        raise HTTPException(
            status_code=500,
            detail=f"Could not save image: {exc}",
        )

    finally:

        await file.close()

    # ----------------------------------------
    # 5. Validate file size
    # ----------------------------------------

    if not validate_file_size(total_size):

        if os.path.exists(upload_path):
            os.remove(upload_path)

        raise HTTPException(
            status_code=413,
            detail="Image exceeds the 50 MB size limit.",
        )

    # ----------------------------------------
    # 6. Validate actual image content
    # ----------------------------------------

    valid, message = validate_image_content(
        upload_path
    )

    if not valid:

        if os.path.exists(upload_path):
            os.remove(upload_path)

        raise HTTPException(
            status_code=400,
            detail=message,
        )

    # ----------------------------------------
    # 7. Generate processed filename
    # ----------------------------------------

    processed_filename = (
        f"{image_id}.png"
    )

    processed_path = os.path.join(
        PROCESSED_DIR,
        processed_filename,
    )

    # ----------------------------------------
    # 8. Preprocess image
    # ----------------------------------------

    try:

        normalize_image(
            upload_path,
            processed_path,
        )

    except Exception as exc:

        if os.path.exists(upload_path):
            os.remove(upload_path)

        raise HTTPException(
            status_code=500,
            detail=f"Image preprocessing failed: {exc}",
        )

    # ----------------------------------------
    # 9. Extract metadata
    # ----------------------------------------

    metadata = extract_metadata(
        upload_path
    )

    # ----------------------------------------
    # 10. Return response
    # ----------------------------------------

    return {
        "success": True,
        "message": "Image uploaded and validated successfully.",
        "image_id": image_id,
        "original_file": original_filename,
        "processed_file": processed_filename,
        "metadata": metadata,
    }