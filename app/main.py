from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="TMM Legends API",
    description="API for Tata Mumbai Marathon Legends Club data",
    version="1.0.0"
)

# Include API routes
app.include_router(router)


@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}
