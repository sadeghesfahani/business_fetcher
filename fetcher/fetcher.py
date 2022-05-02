import json
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from django.utils import timezone

from fetcher.email import Email
from fetcher.fetcher_base import FetcherBase
from bs4 import BeautifulSoup
import requests

from fetcher.models import Page, Business, Person, Activity, URL


class Fetcher(FetcherBase):

    def fetch_all(self):
        next_url = self._url
        companies = list()
        self.all_links = list()
        with open("company_links.txt", 'a', encoding='utf-8') as file:
            while next_url is not None:
                print("page changes\n\n\n")
                html_handler = BeautifulSoup(self._fetch_page(next_url), 'html.parser')
                html_handler = self._purge_html_page(html_handler)
                links = self._extract_links(html_handler)
                self.all_links += links['company']

                # for company in links['company']:
                #     company_html_handler = BeautifulSoup(self._fetch_page(self._convert_to_absolute(company['href'])), 'html.parser')
                #     companies.append(self._analyze_company(company_html_handler))
                next_url = self._base_url + links['next']['href']
                print(next_url)
                # print(links)
                for link in links['company']:
                    file.write(f"{link['href']}\n")
            #
            # with open("companies.txt", "w") as file:
            #     json.dump(companies, file, indent= 4)

    def fetch_business_url(self):
        page = Page.objects.all().first()
        print("fetching page ", page.page)
        if page.finished:
            return None
        url_object = URL.objects.all().first()
        next_url = f"{url_object.url}&page={page.page}"
        page.page += 1
        page.save()
        self.all_links = list()
        page_content, failed = self._fetch_page_for_url(next_url)
        if failed:
            self.get_new_address()
            page.page -= 1
            page.save()
            self.fetch_business_url()
            return None

        html_handler = BeautifulSoup(self._fetch_page(next_url), 'html.parser')
        html_handler = self._purge_html_page(html_handler)
        links = self._extract_links(html_handler)
        self.all_links += links['company']
        if links['next'] is None:
            next_url = None
            print("next page does not found")
        for link in links['company']:

            try:
                company_name = link['href'].split("/")[-1].split("?")[0]
                url_list = link['href'].split("/")[1:-1]
                url_list.append(company_name)
                url_list = "/".join(url_list)
                business_url = self._base_url + "/" + url_list
            except:
                # celery beat off
                pass


            try:
                Business.objects.create(url=business_url, name=company_name.replace('-', " "))
            except:
                # business already exists in database
                pass


    def fetch_business_urls(self):
        page = Page.objects.all().first()
        url_object = URL.objects.all().first()
        next_url = f"{url_object.url}&page={page.page}"
        print(next_url)
        companies = list()
        self.all_links = list()
        html_handler = BeautifulSoup(self._fetch_page(next_url), 'html.parser')
        html_handler = self._purge_html_page(html_handler)
        links = self._extract_links(html_handler)
        self.all_links += links['company']
        if links['next'] is None:
            next_url = None
        else:
            next_url = self._base_url + links['next']['href']
        for link in links['company']:

            try:
                company_name = link['href'].split("/")[-1].split("?")[0]
            except:
                # celery beat off
                pass

            url_list = link['href'].split("/")[1:-1]
            url_list.append(company_name)
            url_list = "/".join(url_list)
            business_url = self._base_url + "/" + url_list
            try:
                Business.objects.create(url=business_url)
            except:
                # business already exists in database
                pass

        page.page += 1
        page.save()

    def fetch_company(self, url):
        html_handler = BeautifulSoup(self._fetch_page(url), 'html.parser')
        html_handler = self._purge_html_page(html_handler)
        self._analyze_company(html_handler, url)

    def _analyze_company(self, html_handler, url):
        business = Business.objects.get(url=url)
        business.in_process = True
        business.save()
        body = self._get_the_body(html_handler)
        header_data = body.contents[1].find("div", {"class": "card"}).find("div", {"class": "h2 text-primary mb-2"}).text
        name = header_data.split("(")[0].strip()
        registery_code = header_data.split("(")[1].strip()[:-1]
        business.name = name
        business.registry_code = registery_code
        info = body.contents[1].find("div", {"class": "card-group row"}).findAll('div')
        left_information = info[0].findAll("div", {"class": "card-body card-body-shrinking"})

        # general information
        general_information = left_information[0]
        status = self._extract_info(general_information, "div", "Status")
        legal_form = self._extract_info(general_information, "div", "Legal form")
        registered = self._extract_info(general_information, "div", "Registered")
        financial_year = self._extract_info(general_information, "div", "Period of the financial year")
        business.status = status
        business.legal_form = legal_form
        business.registered_date = registered
        business.financial_year = financial_year

        # tax information
        tax_information = BeautifulSoup(self._fetch_json(self._base_url + "/eng/company/" + registery_code + "/emta_tax_debt_json")['data']['html'],
                                        "html.parser")
        vat_number = self._extract_info(tax_information, "div", "VAT number").replace("\xa0", " ")
        vat_period = self._extract_info(tax_information, "div", "VAT period").replace("\xa0", " ").replace("– ..", "")
        state_taxes = self._extract_info(tax_information, "div", "State taxes").replace("\xa0", " ").replace(" EUR", "")
        taxes_on_workforce = self._extract_info(tax_information, "div", "Taxes on workforce").replace("\xa0", " ").replace(" EUR", "")
        taxable_turnover = self._extract_info(tax_information, "div", "Taxable turnover").replace("\xa0", " ").replace(" EUR", "")
        number_of_employees = self._extract_info(tax_information, "div", "Number of employees").replace("\xa0", " ")

        business.vat_number = vat_number
        business.vat_period = vat_period
        business.state_taxes = state_taxes
        business.taxes_on_workforce = taxes_on_workforce
        business.taxable_turnover = taxable_turnover
        business.number_of_employees = number_of_employees

        # right part of the page
        right_information = body.contents[1].find("div", {"class": "card-group row"}).findAll("div", {"class": "card col-md-6"})[1].findAll("div", {
            "class": "card-body card-body-shrinking"})
        for x in right_information:
            if self._does_exist(x, "div", "Right of representation"):
                table = x.find('table')
                try:
                    for tr in table.findAll('tr'):
                        tds = tr.findAll('td')
                        if len(tds) > 0:
                            Person.objects.create(business=business, name=tds[0].text.strip(), person_id=tds[1].text.strip(),
                                                  role=tds[2].text.strip())
                except:
                    pass

            # area of activity
            if self._does_exist(x, "div", "Areas of activity"):
                table = x.find('table')
                try:
                    for tr in table.findAll('tr', {"class": "hidden_areasActivity_info"}):
                        td = tr.findAll('td')
                        area_of_activity = dict()

                        area_of_activity['area'] = self._extract_info(td[0], "div", "Area of activity")
                        area_of_activity['EMTAK'] = self._extract_info(td[0], "div", "EMTAK code")
                        area_of_activity['NACE'] = self._extract_info(td[0], "div", "NACE code")
                        area_of_activity['Source'] = self._extract_info(td[0], "div", "Source").replace("\n", " ").replace(
                            "                                     ", " ")
                        Activity.objects.create(business=business, area=area_of_activity['area'], EMTAK_code=area_of_activity['EMTAK'],
                                                NACE_code=area_of_activity['NACE'], source=area_of_activity['Source'])
                except:
                    pass

        # email data

        email_information = BeautifulSoup(self._fetch_json(self._base_url + "/eng/company/" + registery_code + "/tab/registry_card")['data']['html'],
                                          "html.parser")
        email_list = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', str(email_information.contents))
        try:
            business.email = email_list[0]
        except:
            pass

        business.in_process = False
        business.complete = True
        business.last_update = timezone.now()
        business.get_on_next_fetch = False
        business.save()
        print("all done", business.name, business.complete)
        return True

    def fetch_by_name(self, name):
        pass

    def get_new_address(self):
        url = URL.objects.all().first()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://ariregister.rik.ee/eng")
        driver.find_element_by_id("company_search").send_keys("*a*a*a*")
        driver.find_element_by_id("company_search").send_keys(Keys.ENTER)
        time.sleep(3)
        url.url = driver.current_url
        url.save()

        driver.close()
