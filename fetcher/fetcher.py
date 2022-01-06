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
        tax_information = BeautifulSoup(self._fetch_json(self._base_url + "/eng/company/" + registery_code + "/emta_tax_debt_json")['data']['html'],
                                        "html.parser")

        vat_number = self._extract_info(tax_information, "div", "VAT number")
        vat_period = self._extract_info(tax_information, "div", "VAT period")
        state_taxes = self._extract_info(tax_information, "div", "State taxes")
        taxes_on_workforce = self._extract_info(tax_information, "div", "Taxes on workforce")
        taxable_turnover = self._extract_info(tax_information, "div", "Taxable turnover")
        number_of_employees = self._extract_info(tax_information, "div", "Number of employees")

        # right part of the page
        right_information = body.contents[1].find("div", {"class": "card-group row"}).findAll("div", {"class": "card col-md-6"})[1].findAll("div", {
            "class": "card-body card-body-shrinking"})
        for x in right_information:
            if self._does_exist(x, "div", "Right of representation"):
                representations = list()
                table = x.find('table')
                try:
                    for tr in table.findAll('tr'):
                        tds = tr.findAll('td')
                        if len(tds) > 0:
                            person = dict()
                            person['name'] = tds[0].text.strip()
                            person['id'] = tds[1].text.strip()
                            person['role'] = tds[2].text.strip()
                            representations.append(person)
                except:
                    pass
                # print(representations)

            # area of activity
            if self._does_exist(x, "div", "Areas of activity"):
                area_of_activities = list()

                table = x.find('table')
                try:
                    for tr in table.findAll('tr', {"class": "hidden_areasActivity_info"}):
                        td = tr.findAll('td')
                        area_of_activity = dict()
                        area_of_activity['area'] = self._extract_info(td[0], "div", "Area of activity")
                        area_of_activity['EMTAK'] = self._extract_info(td[0], "div", "EMTAK code")
                        area_of_activity['NACE'] = self._extract_info(td[0], "div", "NACE code")
                        area_of_activity['Source'] = self._extract_info(td[0], "div", "Source")
                        area_of_activities.append(area_of_activity)

                        # for div in tr.findAll("div"):
                        #     print(div)
                except:
                    pass

            # others

        # email data
        email_information = BeautifulSoup(self._fetch_json(self._base_url + "/eng/company/" + registery_code + "/tab/registry_card")['data']['html'],
                                          "html.parser")

        # print(financial_year)

        exit()

    def fetch_by_name(self, name):
        pass


new = Fetcher()
new.fetch_all()
