import json
import logging
import requests
from bs4 import BeautifulSoup
from app.services.processing import extract_legends
from app.services.storage import save_json
from app.config import SCRAPE_URL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def scrape_and_store():
    """
    Fetch website data, extract legends records,
    and persist to JSON file.
    """
    logger.info("Scraper started")

    response = requests.get(SCRAPE_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")

    if not script:
        logger.error("Required script tag not found")
        raise Exception("Required script tag not found")

    raw_json = json.loads(script.string)

    year, records = extract_legends(raw_json)

    if not records:
        logger.warning("No records extracted")
        raise Exception("No records extracted")

    filepath = save_json(year, records)

    logger.info(f"Scraper completed. {len(records)} records saved to {filepath}")

    return year, records
