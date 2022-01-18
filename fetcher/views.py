import copy
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.response import Response
from fetcher.fetcher import Fetcher
from fetcher.models import Business
from .serializers import BusinessSerializer

from .tasks import run


class BusinessFetcher(viewsets.ViewSet):

    def jsonify(self, request):
        status = request.GET.get('status')
        name = request.GET.get('name')
        if name is not None:
            query_set = Business.objects.filter(name__icontains=name)
        else:
            if status is not None:
                query_set = Business.objects.filter(status=status, complete=True)
            else:
                query_set = Business.objects.filter(complete=True).exclude(status="Deleted")

        return Response(BusinessSerializer(query_set, many=True).data)
    # def fetch(self, request):
    #     return Response({"hi": "hi"})
    #
    # def fetch_business_url(self,request):
    #     fetcher = Fetcher()
    #     fetcher.fetch_business_urls()
    #
    #
    # def convert_text_to_database(self, request):
    #     print("hi")
    #     with open('fetcher/company_links.txt', 'r', encoding='utf-8') as file:
    #         for company in file.readlines():
    #             company_name = company.split("/")[-1].split("?")[0]
    #             base_url = "https://ariregister.rik.ee/"
    #             url_list = company.split("/")[1:-1]
    #             url_list.append(company_name)
    #
    #             # print(type(url_list))
    #             url_list = "/".join(url_list)
    #             business_url = base_url + url_list
    #             try:
    #                 Business.objects.create(url=business_url)
    #             except:
    #                 pass
    #             # Business.objects.create()
    #     return Response({"hi": "hi"})

    # def start(self,request):
    # interval = IntervalSchedule.objects.all().first()

    # task = PeriodicTask.objects.get_or_create(task='fetcher.tasks.run',interval=interval)

    # return Response(PeriodicTaskSerializer(task[0],many=False).data)
    # task = PeriodicTask.objects.all().first()
    # return Response(PeriodicTaskSerializer(task, many=False).data)


class StartView(TemplateView):
    template_name = 'fetcher/index.html'
