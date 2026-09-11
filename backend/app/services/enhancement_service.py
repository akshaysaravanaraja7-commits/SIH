from pathlib import Path
import time

import cv2

from app.image_handler.preprocessor import normalize_image


class EnhancementService:
    """
    Handles low-light image enhancement.

    Pipeline:
    1. Normalize uploaded image using Member 2 preprocessing.
    2. Apply CLAHE contrast enhancement.
    3. Apply mild brightness correction.
    4. Save enhanced image.
    """

    # --------------------------------------------------
    # Enhance image
    # --------------------------------------------------

    def enhance(
        self,
        input_path: Path,
        output_path: Path
    ) -> dict:
        """
        Enhance a low-light lunar image.

        Member 2 preprocessing is performed before
        Member 1's CLAHE enhancement.
        """

        start_time = time.time()

        # --------------------------------------------------
        # Check input file
        # --------------------------------------------------

        if not input_path.exists():
            raise FileNotFoundError(
                f"Input image not found: {input_path}"
            )

        # --------------------------------------------------
        # Create temporary normalized image
        # --------------------------------------------------

        normalized_path = (
            output_path.parent /
            f"{output_path.stem}_normalized.png"
        )

        try:

            # --------------------------------------------------
            # Member 2 preprocessing
            # --------------------------------------------------

            normalize_image(
                str(input_path),
                str(normalized_path)
            )

            # --------------------------------------------------
            # Read normalized image
            # --------------------------------------------------

            image = cv2.imread(
                str(normalized_path),
                cv2.IMREAD_COLOR
            )

            if image is None:
                raise ValueError(
                    "Unable to read the preprocessed image."
                )

            # --------------------------------------------------
            # Convert BGR → LAB
            # --------------------------------------------------

            lab_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2LAB
            )

            # --------------------------------------------------
            # Split LAB channels
            # --------------------------------------------------

            l_channel, a_channel, b_channel = cv2.split(
                lab_image
            )

            # --------------------------------------------------
            # CLAHE contrast enhancement
            # --------------------------------------------------

            clahe = cv2.createCLAHE(
                clipLimit=2.0,
                tileGridSize=(8, 8)
            )

            enhanced_l = clahe.apply(
                l_channel
            )

            # --------------------------------------------------
            # Merge LAB channels
            # --------------------------------------------------

            enhanced_lab = cv2.merge(
                (
                    enhanced_l,
                    a_channel,
                    b_channel
                )
            )

            # --------------------------------------------------
            # Convert LAB → BGR
            # --------------------------------------------------

            enhanced_image = cv2.cvtColor(
                enhanced_lab,
                cv2.COLOR_LAB2BGR
            )

            # --------------------------------------------------
            # Mild brightness adjustment
            # --------------------------------------------------

            enhanced_image = cv2.convertScaleAbs(
                enhanced_image,
                alpha=1.05,
                beta=8
            )

            # --------------------------------------------------
            # Create output directory
            # --------------------------------------------------

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # --------------------------------------------------
            # Save enhanced image
            # --------------------------------------------------

            success = cv2.imwrite(
                str(output_path),
                enhanced_image
            )

            if not success:
                raise RuntimeError(
                    "Failed to save enhanced image."
                )

        finally:

            # --------------------------------------------------
            # Remove temporary normalized image
            # --------------------------------------------------

            if normalized_path.exists():
                normalized_path.unlink()

        # --------------------------------------------------
        # Processing time
        # --------------------------------------------------

        processing_time = round(
            time.time() - start_time,
            3
        )

        return {
            "status": "completed",
            "output_path": str(output_path),
            "processing_time": processing_time,
            "method": (
                "Member 2 preprocessing + "
                "CLAHE + brightness adjustment"
            ),
        }


# --------------------------------------------------
# Service instance
# --------------------------------------------------

enhancement_service = EnhancementService()