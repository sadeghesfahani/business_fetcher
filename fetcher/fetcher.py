from bs4 import BeautifulSoup

class Fetcher:

    def __init__(self):
        self.url = "https://ariregister.rik.ee/eng/company_search_result/078ae5d"


    def set_url(self, url):
        self.url = url

    def fetch_all(self):
        pass

    def fetch_by_name(self,name):
        pass