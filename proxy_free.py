import requests
from lxml.html import fromstring
import random

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//*[@id="proxylisttable"]/tbody/tr')[200:300]:
        if i.xpath('.//td[7][contains(text(), "yes")]'):
            ip = i.xpath('td[1]/text()')[0]
            port = i.xpath('td[2]/text()')[0]
            proxy = ":".join([ip, port])
            proxies.add(proxy)
    return proxies

if __name__=="__main__":
    proxies = get_proxies()
    print(proxies)
    url = 'https://httpbin.org/ip'

    for proxy in proxies:
        try:
            proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
            response = requests.get(url, proxies=proxies)
            print(response.json())
        except:
            print("Skipping. Connection error")




