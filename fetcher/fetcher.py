import fetcher_base
from bs4 import BeautifulSoup
import requests


class Fetcher(fetcher_base.FetcherBase):

    def fetch_all(self):
        next_url = self._url
        while next_url is not None:

            html_handler = BeautifulSoup(self._fetch_page(next_url), 'html.parser')
            html_handler = self._purge_html_page(html_handler)
            links = self._extract_links(html_handler)
            for company in links['company']:
                company_html_handler = BeautifulSoup(self._fetch_page(self._convert_to_absolute(company['href'])), 'html.parser')
                self._analyze_company(company_html_handler)
            next_url = links['next']['href']

    def _analyze_company(self, html_handler):
        html_handler = self._purge_html_page(html_handler)

    def fetch_by_name(self, name):
        pass


new = Fetcher()
new.fetch_all()
