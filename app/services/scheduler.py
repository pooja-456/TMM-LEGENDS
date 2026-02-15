from apscheduler.schedulers.background import BackgroundScheduler
from app.services.scraper_service import scrape_and_store

scheduler = BackgroundScheduler()


def start_scheduler(interval_hours: int):
    scheduler.add_job(
        scrape_and_store,
        "interval",
        hours=interval_hours
    )

    scheduler.start()
