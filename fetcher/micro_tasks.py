from business_fetcher import celery_app
from fetcher.fetcher import Fetcher


@celery_app.task(bind=True)
def fetch_business(url):
    Fetcher().fetch_company(url)


@celery_app.task()
def fetch_url():
    Fetcher().fetch_business_url()
