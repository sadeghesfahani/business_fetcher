


@celery_app.task(bind=True)
def fetch_business(url):
    Fetcher().fetch_company(url)


@celery_app.task(name="hi")
def fetch_url():
    Fetcher().fetch_business_url()
