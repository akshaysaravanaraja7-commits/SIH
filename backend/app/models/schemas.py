from typing import Optional

from pydantic import BaseModel, Field


# --------------------------------------------------
# Upload response
# --------------------------------------------------

class UploadResponse(BaseModel):
    image_id: str = Field(
        ...,
        description="Unique identifier assigned to the uploaded image"
    )

    filename: str = Field(
        ...,
        description="Original uploaded filename"
    )

    status: str = Field(
        ...,
        description="Current processing status"
    )

    message: str = Field(
        ...,
        description="Human-readable response message"
    )


# --------------------------------------------------
# Enhancement response
# --------------------------------------------------

class EnhancementResponse(BaseModel):
    image_id: str = Field(
        ...,
        description="Unique image identifier"
    )

    status: str = Field(
        ...,
        description="Current enhancement status"
    )

    message: str = Field(
        ...,
        description="Human-readable response message"
    )


# --------------------------------------------------
# Status response
# --------------------------------------------------

class StatusResponse(BaseModel):
    image_id: str = Field(
        ...,
        description="Unique image identifier"
    )

    status: str = Field(
        ...,
        description="Current processing status"
    )

    progress: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Processing progress from 0 to 100"
    )

    message: Optional[str] = Field(
        default=None,
        description="Additional processing information"
    )


# --------------------------------------------------
# Error response
# --------------------------------------------------

class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="Error type"
    )

    message: str = Field(
        ...,
        description="Detailed error message"
    )