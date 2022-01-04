from bs4 import BeautifulSoup
import requests


class Fetcher:

    def __init__(self):
        self._url = "https://ariregister.rik.ee/eng/company_search_result/078ae5d"

    def set_url(self, url):
        self._url = url

    def fetch_all(self):
        html_handler = BeautifulSoup(self._fetch_page(self._url), 'html.parser')
        html_handler = self._purge_html_page(html_handler)
        links = self._extract_links(html_handler)

    def fetch_by_name(self, name):
        pass


    def _extract_links(self,html_handler):
        for links in html_handler.findAll('a'):
            print(links)
        return None
    def _fetch_page(self, url):
        response = requests.get(url)
        return response.text

    @staticmethod
    def _purge_html_page(html_handler_object):
        [x.extract() for x in html_handler_object.findAll('script')]
        return html_handler_object


new = Fetcher()
new.fetch_all()
