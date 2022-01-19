import requests

http_proxy = "http://alimzd:d5gp7TGtIuvzQ3F6@proxy.packetstream.io:31112"
https_proxy = "http://alimzd:d5gp7TGtIuvzQ3F6@proxy.packetstream.io:31112"
url = "https://ipv4.icanhazip.com"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
}

r = requests.get(url, proxies=proxyDict)