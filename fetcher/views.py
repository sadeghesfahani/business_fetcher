import copy

from rest_framework import viewsets
from rest_framework.response import Response
from fetcher.fetcher import Fetcher
from fetcher.models import Business


class BusinessFetcher(viewsets.ViewSet):

    def fetch(self, request):
        return Response({"hi": "hi"})

    def fetch_business_url(self,request):
        fetcher = Fetcher()
        fetcher.fetch_business_urls()


    def convert_text_to_database(self, request):
        print("hi")
        with open('fetcher/company_links.txt', 'r', encoding='utf-8') as file:
            for company in file.readlines():
                company_name = company.split("/")[-1].split("?")[0]
                base_url = "https://ariregister.rik.ee/"
                url_list = company.split("/")[1:-1]
                url_list.append(company_name)

                # print(type(url_list))
                url_list = "/".join(url_list)
                business_url = base_url + url_list
                try:
                    Business.objects.create(url=business_url)
                except:
                    pass
                # Business.objects.create()
        return Response({"hi": "hi"})
