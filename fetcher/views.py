from rest_framework import viewsets
from rest_framework.response import Response


class BusinessFetcher(viewsets.ViewSet):

    def fetch(self,request):
        return Response({"hi":"hi"})