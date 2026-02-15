import requests
import json
from bs4 import BeautifulSoup
from app.services.processing import extract_legends
from app.services.storage import save_json

URL = "https://tatamumbaimarathon.procam.in/initiatives/tmm-legends-club"


def scrape_and_store():
    print("=== SCRAPER STARTED ===")

    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    print("=== PAGE FETCHED ===")

    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")

    if not script:
        print("ERROR: Script tag not found")
        raise Exception("Required script tag not found")

    raw_json = json.loads(script.string)

    print("=== RAW JSON LOADED ===")

    year, records = extract_legends(raw_json)

    print(f"Year detected: {year}")
    print(f"Records extracted: {len(records)}")

    if not records:
        print("WARNING: No records extracted")
        raise Exception("No records extracted")

    filepath = save_json(year, records)

    print(f"JSON saved at: {filepath}")
    print("=== SCRAPER COMPLETED ===")

    return year, records
