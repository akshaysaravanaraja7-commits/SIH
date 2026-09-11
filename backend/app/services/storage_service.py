from pathlib import Path

from app.config import UPLOAD_DIR, OUTPUT_DIR


class StorageService:
    """
    Handles file storage operations for uploaded
    and enhanced images.
    """

    # --------------------------------------------------
    # Upload storage
    # --------------------------------------------------

    def save_upload(
        self,
        source_path: Path,
        destination_name: str
    ) -> Path:
        """
        Copy an existing file into the uploads directory.
        """

        destination = UPLOAD_DIR / destination_name

        destination.write_bytes(
            source_path.read_bytes()
        )

        return destination

    # --------------------------------------------------
    # Check uploaded file
    # --------------------------------------------------

    def upload_exists(
        self,
        filename: str
    ) -> bool:
        """
        Check whether an uploaded file exists.
        """

        return (
            UPLOAD_DIR / filename
        ).exists()

    # --------------------------------------------------
    # Find uploaded image
    # --------------------------------------------------

    def find_upload(
        self,
        image_id: str
    ) -> Path | None:
        """
        Find an uploaded image using its image ID.
        """

        files = list(
            UPLOAD_DIR.glob(
                f"{image_id}.*"
            )
        )

        if not files:
            return None

        return files[0]

    # --------------------------------------------------
    # Find enhanced image
    # --------------------------------------------------

    def find_output(
        self,
        image_id: str
    ) -> Path | None:
        """
        Find an enhanced image using its image ID.
        """

        files = list(
            OUTPUT_DIR.glob(
                f"{image_id}_enhanced.*"
            )
        )

        if not files:
            return None

        return files[0]

    # --------------------------------------------------
    # Delete uploaded image
    # --------------------------------------------------

    def delete_upload(
        self,
        image_id: str
    ) -> bool:
        """
        Delete an uploaded image.
        """

        file_path = self.find_upload(
            image_id
        )

        if file_path is None:
            return False

        file_path.unlink()

        return True

    # --------------------------------------------------
    # Delete enhanced image
    # --------------------------------------------------

    def delete_output(
        self,
        image_id: str
    ) -> bool:
        """
        Delete an enhanced image.
        """

        file_path = self.find_output(
            image_id
        )

        if file_path is None:
            return False

        file_path.unlink()

        return True

    # --------------------------------------------------
    # Get storage information
    # --------------------------------------------------

    def get_storage_info(self) -> dict:
        """
        Return basic storage information.
        """

        upload_files = list(
            UPLOAD_DIR.iterdir()
        )

        output_files = list(
            OUTPUT_DIR.iterdir()
        )

        return {
            "upload_directory": str(
                UPLOAD_DIR
            ),
            "output_directory": str(
                OUTPUT_DIR
            ),
            "uploaded_files": len(
                upload_files
            ),
            "enhanced_files": len(
                output_files
            ),
        }


# --------------------------------------------------
# Service instance
# --------------------------------------------------

storage_service = StorageService()