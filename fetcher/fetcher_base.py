import re

import requests
from requests.auth import HTTPBasicAuth
from fetcher.porxy import Proxy


class FetcherBase:
    def __init__(self):
        self._url = "https://ariregister.rik.ee/eng/company_search_result/4bec816?name_or_code=%2Aa%2Aa%2Aa"
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

                if "Next" in link.text:
                    links['next'] = link
        return links

    def _fetch_page(self, url):
        proxy = Proxy().get()
        if proxy:
            proxy_dict = {
                "http": proxy,
                "https": proxy,
            }
            try:
                response = requests.get(url, proxies=proxy_dict)
            except:
                response = requests.get(url)
        else:
            response = requests.get(url)
        return response.text

    def _fetch_json(self, url):
        headers = {"Host": "ariregister.rik.ee"}
        proxy = Proxy().get()
        if proxy:
            proxy_dict = {
                "http": proxy,
                "https": proxy,
            }
            try:

                response = requests.get(url, headers=headers, proxies=proxy_dict)
                print(response)
            except:
                response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        return response.json()

    def _fetch_page_for_url(self, url):
        proxy = Proxy().get()
        if proxy:
            proxy_dict = {
                "http": proxy,
                "https": proxy,
            }
            try:
                response = requests.get(url, proxies=proxy_dict)
            except:
                response = requests.get(url)
        else:
            response = requests.get(url)
        redirected = False
        if response.history == 303:
            redirected = True
        return response.text, redirected

    @staticmethod
    def _purge_html_page(html_handler_object):
        [x.extract() for x in html_handler_object.findAll('script')]
        return html_handler_object

    def _get_the_body(self, html_handler_object):
        return html_handler_object.find("div", {"class": "ar__center__bg"})

    def _determine_which_part_is_it(self, html_handler):
        pass

    def _extract_info(self, html_handler, tag_type, info):
        info_tag = html_handler.find(tag_type, text=re.compile(info))
        try:
            return info_tag.find_next_sibling(tag_type).text.strip()
        except:
            return ""

    def _does_exist(self, html_handler, tag_type, info):
        # print(info)
        # print(html_handler, "\n\n\n\n\n\n\n")
        for tag in html_handler.findAll("div"):
            if info in tag.text:
                return True
        return False
        # info_tag = html_handler.find(tag_type, text=re.compile(info))
        # print(info_tag)
        # if info_tag is not None:
        #     return True
        # return False
