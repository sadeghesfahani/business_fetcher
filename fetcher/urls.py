from .views import BusinessFetcher
from django.urls import path

urlpatterns = [
    path('fetch/', BusinessFetcher.as_view({"get": "fetch"}), name="fetch"),
]
