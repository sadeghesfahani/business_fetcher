from DJANGO_PROJECT.settings import JOBSPERTASK
from fetcher.models import Business, Page, URL
# from fetcher.fetcher import Fetcher
from fetcher.micro_tasks import fetch_business, fetch_url


class ActiveTasks:
    def __init__(self):
        self.business = Business
        self.page = Page

    def get_tasks(self):
        tasks = list()
        reminded_jobs = JOBSPERTASK
        page = self.page.objects.all().first()
        url_object = URL.objects.all().first()
        if not page.finished and not url_object.failed:
            tasks.append([fetch_url, None])
            reminded_jobs -= 1
        businesses = list(self.business.objects.filter(get_on_next_fetch=True))
        reminded_jobs -= len(businesses)
        if reminded_jobs > 0:
            businesses += self.business.objects.filter(complete=False, in_process=False)[:reminded_jobs]
        for business in businesses:
            tasks.append([fetch_business, business.url])
        return tasks
