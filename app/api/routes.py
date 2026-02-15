from fastapi import APIRouter, HTTPException
from app.services.scraper_service import scrape_and_store
from app.services.storage import load_json

router = APIRouter()


@router.get("/", tags=["System"])
def root():
    """
    Root endpoint to verify API availability.
    """
    return {"message": "TMM Legends API is running"}


@router.get("/scrape-now", tags=["Scraper"])
def scrape_now():
    """
    Manually trigger scraper and persist latest data.
    """
    try:
        year, records = scrape_and_store()
        return {
            "year": year,
            "records_saved": len(records)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/legends", tags=["Data"])
def get_legends(year: int | None = None):
    """
    Retrieve legends data.
    If year is not provided, latest available dataset is returned.
    """
    return load_json(year)
