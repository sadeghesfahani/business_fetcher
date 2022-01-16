from business_fetcher.settings import JOBSPERTASK
from fetcher.models import Business, Page
# from fetcher.fetcher import Fetcher
from fetcher.micro_tasks import fetch_business, fetch_url


class ActiveTasks:
    def __init__(self):
        self.business = Business
        self.page = Page

    def get_tasks(self):
        tasks = list()
        reminded_jobs = JOBSPERTASK
        print("im here -----------------------------------------------------------")
        page = self.page.objects.first()
        print(page)
        if not self.page.objects.first().finished:
            tasks.append([fetch_url, None])
            reminded_jobs -= 1
        print("alsooooooooooooooim here -----------------------------------------------------------")
        businesses = self.business.objects.filter(complete=False, in_process=False)[:reminded_jobs]
        for business in businesses:
            tasks.append([fetch_business, business.url])
        return tasks
