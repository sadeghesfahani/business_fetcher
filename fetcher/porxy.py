import time
from datetime import timedelta

from django.utils import timezone


class Proxy:
    def __init__(self):
        self.proxy_pool = []
        self.proxy_dictionary = dict()
        self.interval = 20
        self.fail_limit = 10
        self.allowed_eccentricity = 10
        self.sleep_time = 10

    def _initial_proxy_dictionary(self):
        for proxy in self.proxy_pool:
            self.proxy_dictionary[proxy] = {"last_use": None, "number_of_usage": 0, "number_of_fails": 0}

    def _set_proxy_pool(self):
        pass

    def get_proxy(self):
        for proxy in self.proxy_dictionary.keys():
            if self._is_proxy_available(proxy):
                return proxy
        time.sleep(self.sleep_time)
        return self.get_proxy()

    def _is_proxy_available(self, proxy):
        if timezone.now() - self.proxy_dictionary[proxy]["last_user"] > timedelta(seconds=self.interval):
            if self.proxy_dictionary[proxy]['number_of_fails'] < self.fail_limit:
                if self.proxy_dictionary[proxy]['number_of_usage'] - self._average_usage() < self.allowed_eccentricity:
                    return True
        return False

    def _average_usage(self):
        summation = 0
        for proxy in self.proxy_dictionary.keys():
            summation += self.proxy_dictionary[proxy]['number_of_usage']

        return summation / len(self.proxy_dictionary)
