from pathlib import Path

from fastapi import APIRouter

from app.config import (
    UPLOAD_DIR,
    OUTPUT_DIR,
)


# --------------------------------------------------
# API Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Health"]
)


# --------------------------------------------------
# System health
# --------------------------------------------------

@router.get("/health")
async def health_check():
    """
    Check whether the backend and required storage
    directories are available.
    """

    upload_ready = (
        UPLOAD_DIR.exists()
        and UPLOAD_DIR.is_dir()
    )

    output_ready = (
        OUTPUT_DIR.exists()
        and OUTPUT_DIR.is_dir()
    )

    system_ready = (
        upload_ready
        and output_ready
    )

    return {
        "status": "healthy" if system_ready else "degraded",
        "service": "lunar-image-enhancement-api",
        "storage": {
            "uploads": upload_ready,
            "outputs": output_ready,
        }
    }