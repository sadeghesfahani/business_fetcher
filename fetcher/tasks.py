from business_fetcher import celery_app
from fetcher.models import Page


@celery_app.task()
def get_business_links():
    page = Page.objects.all().first().page



