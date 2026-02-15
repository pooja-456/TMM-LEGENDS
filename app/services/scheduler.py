from apscheduler.schedulers.background import BackgroundScheduler
from app.services.scraper_service import scrape_and_store

scheduler = BackgroundScheduler()


def start_scheduler(interval_hours: int):
    """
    Start background scheduler for periodic scraping.
    """
    scheduler.add_job(
        scrape_and_store,
        trigger="interval",
        hours=interval_hours
    )

    scheduler.start()
