from .views import BusinessFetcher, StartView
from django.urls import path

urlpatterns = [
    path('json/', BusinessFetcher.as_view({"get": "jsonify"}), name="jsonify"),
    # path('fetch/', BusinessFetcher.as_view({"get": "fetch"}), name="fetch"),
    # path('convert/', BusinessFetcher.as_view({"get": "convert_text_to_database"}), name="convert"),
    # path('fetch_url/', BusinessFetcher.as_view({"get": "fetch_business_url"}), name="fetch-url"),
    # path('start/', BusinessFetcher.as_view({"get": "start"}), name="start-fetching"),
    path('', StartView.as_view(), name="home"),
]
