import requests


class FetcherBase:
    def __init__(self):
        self._url = "https://ariregister.rik.ee/eng/company_search_result/078ae5d"
        self._base_url = "https://ariregister.rik.ee"

    def set_url(self, url):
        self._url = url

    def _convert_to_absolute(self, url):
        return self._base_url + url

    def _extract_links(self, html_handler):
        links = dict()
        links['company'] = list()
        links['next'] = None
        for link in html_handler.findAll('a'):
            href = link['href']
            if href[:13] == "/eng/company/":
                links['company'].append(link)
            else:
                if link.text == "Next":
                    links['next'] = link
        return links

    def _fetch_page(self, url):
        response = requests.get(url)
        return response.text

    @staticmethod
    def _purge_html_page(html_handler_object):
        [x.extract() for x in html_handler_object.findAll('script')]
        return html_handler_object
