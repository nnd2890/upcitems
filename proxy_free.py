import requests
from lxml.html import fromstring
import random

def get_proxies_new():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//*[@id="proxylisttable"]/tbody/tr'):
        if i.xpath('.//td[7][contains(text(), "yes")]'):
            ip = i.xpath('td[1]/text()')[0]
            port = i.xpath('td[2]/text()')[0]
            proxy = ":".join([ip, port])
            proxies.add(proxy)
    print('new: ', len(proxies))
    return proxies

def get_proxies_usa():
    url = 'https://www.us-proxy.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//*[@id="proxylisttable"]/tbody/tr'):
        if i.xpath('.//td[7][contains(text(), "yes")]'):
            ip = i.xpath('td[1]/text()')[0]
            port = i.xpath('td[2]/text()')[0]
            proxy = ":".join([ip, port])
            proxies.add(proxy)
    print('usa: ', len(proxies))
    return proxies

def get_proxies_sock():
    url = 'https://www.socks-proxy.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//*[@id="proxylisttable"]/tbody/tr'):
        if i.xpath('.//td[7][contains(text(), "Yes")]'):
            ip = i.xpath('td[1]/text()')[0]
            port = i.xpath('td[2]/text()')[0]
            proxy = ":".join([ip, port])
            proxies.add(proxy)
    print('sock: ', len(proxies))
    return proxies

def get_proxies_ssl():
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//*[@id="proxylisttable"]/tbody/tr'):
        if i.xpath('.//td[7][contains(text(), "yes")]'):
            ip = i.xpath('td[1]/text()')[0]
            port = i.xpath('td[2]/text()')[0]
            proxy = ":".join([ip, port])
            proxies.add(proxy)
    print('ssl: ', len(proxies))
    return proxies

def get_proxies():
    proxies_new = get_proxies_new()
    proxies_new.update(get_proxies_usa())
    # proxies_new.update(get_proxies_sock())
    proxies_new.update(get_proxies_ssl())
    #
    print('all proxies: ',len(proxies_new))
    return proxies_new

def check_proxy():
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

if __name__=="__main__":

    print(get_proxies_ssl())




