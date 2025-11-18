from celery import Celery
from celery.schedules import crontab
from scraper.scrape import scrape_all

# Celery configuration
celery = Celery(
    "my_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery.conf.timezone = "UTC"
celery.conf.enable_utc = True

@celery.task
def scraper():
    print("Cron Job Started!")
    scrape_all()
    print("Cron Job Finished!")

# CELERY BEAT SCHEDULE
celery.conf.beat_schedule = {
    "run-every-8-hours": {
        "task": "celery_app.scraper",
        "schedule": crontab(), 
    },
}
