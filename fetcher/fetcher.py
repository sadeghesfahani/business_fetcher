import re

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
        body = self._get_the_body(html_handler)
        header_data = body.contents[1].find("div", {"class": "card"}).find("div", {"class": "h2 text-primary mb-2"}).text
        name = header_data.split("(")[0].strip()
        registery_code = header_data.split("(")[1].strip()[:-1]
        info = body.contents[1].find("div", {"class": "card-group row"}).findAll('div')
        left_information = info[0].findAll("div", {"class": "card-body card-body-shrinking"})

        # general information
        general_information = left_information[0]
        status = self._extract_info(general_information, "div", "Status")
        legal_form = self._extract_info(general_information, "div", "Legal form")
        registered = self._extract_info(general_information, "div", "Registered")
        financial_year = self._extract_info(general_information, "div", "Period of the financial year")

        # tax information
        print(self._base_url + "/eng/company/" + registery_code + "/emta_tax_debt_json")
        tax_information = BeautifulSoup(self._fetch_json(self._base_url + "/eng/company/" + registery_code + "/emta_tax_debt_json")['data']['html'], "html.parser")
        vat_number = self._extract_info(tax_information, "div", "VAT number")
        vat_period = self._extract_info(tax_information, "div", "VAT period")
        state_taxes = self._extract_info(tax_information, "div", "State taxes")
        taxes_on_workforce = self._extract_info(tax_information, "div", "Taxes on workforce")
        taxable_turnover = self._extract_info(tax_information, "div", "Taxable turnover")
        number_of_employees = self._extract_info(tax_information, "div", "Number of employees")
        print(number_of_employees)




        # print(financial_year)

        exit()

    def _extract_info(self, html_handler, tag_type, info):
        info_tag = html_handler.find(tag_type, text=re.compile(info))
        return info_tag.find_next_sibling(tag_type).text.strip()

    def fetch_by_name(self, name):
        pass


new = Fetcher()
new.fetch_all()
