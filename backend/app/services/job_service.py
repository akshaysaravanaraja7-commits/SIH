from datetime import datetime, timezone
from threading import Lock


class JobService:
    """
    In-memory service for tracking image processing jobs.

    This is suitable for the prototype.
    A database or Redis can replace this later if needed.
    """

    def __init__(self):
        self._jobs = {}
        self._lock = Lock()

    # --------------------------------------------------
    # Create job
    # --------------------------------------------------

    def create_job(
        self,
        image_id: str,
        filename: str
    ) -> dict:
        """
        Create a new processing job.
        """

        job = {
            "image_id": image_id,
            "filename": filename,
            "status": "uploaded",
            "progress": 0,
            "message": "Image uploaded successfully.",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "updated_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        with self._lock:
            self._jobs[image_id] = job

        return job

    # --------------------------------------------------
    # Get job
    # --------------------------------------------------

    def get_job(
        self,
        image_id: str
    ) -> dict | None:
        """
        Return a job by image ID.
        """

        with self._lock:
            return self._jobs.get(image_id)

    # --------------------------------------------------
    # Update job
    # --------------------------------------------------

    def update_job(
        self,
        image_id: str,
        status: str | None = None,
        progress: int | None = None,
        message: str | None = None
    ) -> dict | None:
        """
        Update the state of an existing job.
        """

        with self._lock:
            job = self._jobs.get(image_id)

            if job is None:
                return None

            if status is not None:
                job["status"] = status

            if progress is not None:
                job["progress"] = max(
                    0,
                    min(progress, 100)
                )

            if message is not None:
                job["message"] = message

            job["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            return job


# --------------------------------------------------
# Service instance
# --------------------------------------------------

job_service = JobService()