from fastapi import APIRouter
from app.services.scraper_service import scrape_and_store
from app.services.storage import load_json

router = APIRouter()
print("ROUTES FILE LOADED")

@router.get("/")
def root():
    return {"message": "TMM Legends API is running"}

@router.get("/scrape-now")
def scrape_now():
    year, records = scrape_and_store()
    return {
        "year": year,
        "records_saved": len(records)
    }

@router.get("/legends")
def get_legends():
    return load_json()
