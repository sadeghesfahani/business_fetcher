from DJANGO_PROJECT import celery_app
from fetcher.fetcher import Fetcher


@celery_app.task(bind=True)
def fetch_business(url,*args,**kwargs):
    Fetcher().fetch_company(args[0])


@celery_app.task()
def fetch_url():
    Fetcher().fetch_business_url()
