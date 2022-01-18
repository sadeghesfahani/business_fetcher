# import requests
# from requests.auth import HTTPBasicAuth
#
# proxy_dict = {
#     "http": "http://alimzd:d5gp7TGtIuvzQ3F6@proxy.packetstream.io:31112",
#     "https": "http://alimzd:d5gp7TGtIuvzQ3F6@proxy.packetstream.io:31111",
# }
#
# response = requests.get('https://ipv4.icanhazip.com', verify=False, proxies=proxy_dict, auth=('alimzd','13761379'))
# print(response.__dict__)



import requests

http_proxy = "http://alimzd:d5gp7TGtIuvzQ3F6@proxy.packetstream.io:31112"
https_proxy = "https://alimzd:d5gp7TGtIuvzQ3F6@proxy.packetstream.io:31111"
url = "http://ipv4.icanhazip.com"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
}

r = requests.get(url, proxies=proxyDict)
print(r.__dict__)