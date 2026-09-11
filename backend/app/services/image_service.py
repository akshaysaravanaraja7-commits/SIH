from pathlib import Path

from fastapi import UploadFile

from app.config import (
    MAX_FILE_SIZE_BYTES,
    UPLOAD_DIR,
)
from app.utils.file_utils import (
    generate_image_id,
    get_upload_path,
)


class ImageService:
    """
    Service responsible for storing and managing
    uploaded images.
    """

    # --------------------------------------------------
    # Save uploaded image
    # --------------------------------------------------

    async def save_uploaded_image(
        self,
        file: UploadFile
    ) -> dict:
        """
        Save an uploaded image safely using chunks.

        The upload is rejected if it exceeds the
        configured maximum file size.
        """

        # --------------------------------------------------
        # Validate filename
        # --------------------------------------------------

        if not file.filename:
            raise ValueError(
                "Uploaded file has no filename."
            )

        # --------------------------------------------------
        # Generate image ID
        # --------------------------------------------------

        image_id = generate_image_id()

        # --------------------------------------------------
        # Create upload path
        # --------------------------------------------------

        upload_path = get_upload_path(
            image_id,
            file.filename
        )

        total_size = 0

        try:
            # --------------------------------------------------
            # Open destination file
            # --------------------------------------------------

            with upload_path.open("wb") as destination:

                while True:

                    # Read 1 MB at a time
                    chunk = await file.read(
                        1024 * 1024
                    )

                    # No more data
                    if not chunk:
                        break

                    total_size += len(chunk)

                    # --------------------------------------------------
                    # Check file size
                    # --------------------------------------------------

                    if total_size > MAX_FILE_SIZE_BYTES:

                        # Remove incomplete file
                        destination.close()

                        if upload_path.exists():
                            upload_path.unlink()

                        raise ValueError(
                            "File is too large. "
                            f"Maximum allowed size is "
                            f"{MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
                        )

                    destination.write(chunk)

        except ValueError:
            raise

        except Exception as error:

            # Remove incomplete file if something failed
            if upload_path.exists():
                upload_path.unlink()

            raise RuntimeError(
                f"Failed to save uploaded image: {error}"
            )

        finally:
            await file.close()

        # --------------------------------------------------
        # Make sure something was uploaded
        # --------------------------------------------------

        if total_size == 0:

            if upload_path.exists():
                upload_path.unlink()

            raise ValueError(
                "Uploaded file is empty."
            )

        # --------------------------------------------------
        # Return information
        # --------------------------------------------------

        return {
            "image_id": image_id,
            "filename": file.filename,
            "file_path": str(upload_path),
            "file_size": total_size,
            "content_type": file.content_type,
        }

    # --------------------------------------------------
    # Find uploaded image
    # --------------------------------------------------

    def get_image_path(
        self,
        image_id: str
    ) -> Path | None:
        """
        Find an uploaded image using its image ID.
        """

        matching_files = list(
            UPLOAD_DIR.glob(
                f"{image_id}.*"
            )
        )

        if not matching_files:
            return None

        return matching_files[0]

    # --------------------------------------------------
    # Check whether image exists
    # --------------------------------------------------

    def image_exists(
        self,
        image_id: str
    ) -> bool:
        """
        Check whether an uploaded image exists.
        """

        return self.get_image_path(
            image_id
        ) is not None


# --------------------------------------------------
# Service instance
# --------------------------------------------------

image_service = ImageService()