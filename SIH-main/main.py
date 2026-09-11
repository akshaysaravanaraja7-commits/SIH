from fastapi import FastAPI

from api.enhancement import router as enhancement_router


app = FastAPI(
    title="Lunar PSR Image Enhancement API",
    description=(
        "Backend API for low-light image enhancement "
        "of Permanently Shadowed Regions (PSRs) "
        "of lunar craters."
    ),
    version="1.0.0",
)


app.include_router(enhancement_router)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Lunar PSR Image Enhancement API is running.",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }