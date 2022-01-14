import datetime

from django.utils import timezone

from fetcher.models import Proxy as ProxyModel


class Proxy:
    def __init__(self):
        self.proxy = ProxyModel

    def get(self):
        try:
            proxy = self.proxy.objects.all().order_by('-last_used_date').first()
            proxy.last_used_date = timezone.now()
            proxy.save()
            return proxy.proxy
        except:
            return False
