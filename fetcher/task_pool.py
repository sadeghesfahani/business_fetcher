from business_fetcher.settings import JOBSPERTASK
from fetcher.models import Business, Page
from fetcher.fetcher import Fetcher


class ActiveTasks:
    def __init__(self):
        self.business = Business
        self.page = Page

    def get_tasks(self):
        tasks = list()
        reminded_jobs = JOBSPERTASK
        if not self.page.objects.first().finished:
            tasks.append(Fetcher().fetch_business_url)
            reminded_jobs -= 1

        businesses = self.business.objects.filter(complete=False, in_process=False)[:reminded_jobs]
        for job in businesses:
            tasks.append(Fetcher())
