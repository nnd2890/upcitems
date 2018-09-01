import urllib.parse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lxml import html
import unicodecsv as csv
from multiprocessing import Pool as ThreadPool
import sys, os
import json
import time
import proxy_free
import random
from user_agent import generate_user_agent
import datetime
from my_module import *
import csv
from database_mysql import MysqlDatabase

def parse_listing(url):
    headers = {'user-agent':generate_user_agent(os=('mac', 'linux'), device_type="desktop")}
    scraped_results = []
    try:

        times = [0,0.2,0.4,0.6,0.8,1]
        # times = [5,6,7,8,9,10]
        time.sleep(random.choice(times))
        print('parsing page: ' + url)
        response = get_response(url)

        # proxy_list = get_share_proxies()
        # random_proxy = get_random_proxy(proxy_list)
        # proxies = {"http": "http://" + random_proxy, "https": "http://" + random_proxy}
        # s = requests.session()
        # s.cookies.clear()
        # response = s.get = requests.get(url, verify=False, headers = headers, timeout=10, proxies=proxies)
        print("parsed page: " + url)
        if response.status_code == 200:
            parser = html.fromstring(response.text)

            XPATH_LISTINGS = '//div[contains(@class,"upclist")]/ul/li'
            listings = parser.xpath(XPATH_LISTINGS)
            for results in listings[0:1]:
                XPATH_searched_upc = './/div/a/text()'
                XPATH_searched_name = './/div/p/text()'

                searched_upc = get_string(results, XPATH_searched_upc)
                searched_name = get_string(results, XPATH_searched_name)
                
                business_details = {
                    'searched_upc':searched_upc,
                    'searched_name':searched_name,
                    'url':url,
                }

                if True:
                    scraped_results.append(business_details)
            return  scraped_results
        elif response.status_code == 404:
            print("Could not find a location matching", response.status_code)
            business_details = {
                'searched_upc': 'N/A',
                'searched_name': 'N/A',
                'url': url,
            }

            if True:
                scraped_results.append(business_details)
            return scraped_results
        else:
            print("Failed to process page", response.status_code)
            return []
    except Exception as e:
        print("Failed to process page:", e)
        exc_type, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return []

def get_random_proxy(proxies):
    return random.sample(set(proxies), 1)[0]


def get_share_proxies():
    with open("proxies_http_ip.csv", 'r') as csv_file:
        reader = list(csv.reader(csv_file))
        number = len(reader) - 1
        proxy_list = []
        for row in reader:
            proxy_list.append(row[0])
        return proxy_list

def get_response(url):
    headers = {'user-agent':generate_user_agent(os=('mac', 'linux'), device_type="desktop")}
    proxylist = proxy_free.get_proxies()
    response = ''
    running = True
    if proxylist:
        while running:
            for proxy in proxylist:
                try:
                    proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
                    s = requests.session()
                    s.cookies.clear()
                    response = s.get(url, verify=False, headers = headers, timeout=10, proxies=proxies)
                    if response.status_code == 429:
                        continue
                    print('worked %s' % proxy)
                    running = False
                    break
                except requests.exceptions.Timeout:
                    continue
                except Exception as e:
                    print ('error %s' % proxy)
                    print ('error %s' % e)
    else:
        response = requests.get(url, verify=False, headers = headers, timeout=10)

    return response

def pool_scraped_data(function_name, parameter_list):
    pool = ThreadPool(2)
    scraped_data = pool.map(function_name, parameter_list)
    pool.terminate()
    pool.join()
    return scraped_data

def pool(function_name, parameter_list):
    pool = ThreadPool(10)
    pool.map(function_name, parameter_list)
    pool.terminate()
    pool.join()


def get_url_list(name_list):
    url_list = []
    for name in name_list:
        url = 'https://www.upcitemdb.com/query?type=2&s=' + name
        url_list.append(url)
    return url_list

def get_url(name):
    url = 'https://www.upcitemdb.com/query?type=2&s=' + name
    return url

def insert_to_database_csv():
    upc_database = MysqlDatabase()
    table = 'upc'
    with open("odskek.csv", 'r') as csv_file:
        reader = list(csv.reader(csv_file))
        print(len(reader))
        i=1
        for row in reader[100:200]:
            name = row[0].split(',')[0]
            col = 'name'
            try:
                if upc_database.row_existed(table, col, name):
                    print('Row exsited.')
                else:
                    data = {
                        'name': name,
                    }
                    print('Row inserted.' + name)
                    print('Row number: ' + i)
                    upc_database.insertRow(table, data)
            except:
                continue
            i = i + 1

def update_mysql(name):
    try:
        upc_database = MysqlDatabase()
        table = 'upc2'
        col = 'name'
        url = get_url(name)
        scraped_data = parse_listing(url)
        if scraped_data:
            upc_database.update_row(table, scraped_data[0], col, name)
            print(scraped_data)
    except Exception as e:
        print('Error insert to mysql: ' + e)



if __name__=="__main__":

    upc_database = MysqlDatabase()
    table = 'upc2'
    running = True
    while running:
        null_records = upc_database.select_all_is_null(table,'searched_name')
        try:
            if null_records:
                name_list = []
                for null_record in null_records:
                    name_list.append(null_record[0])
                pool(update_mysql, name_list)
                print(name_list)
            else:
                running = False
        except Exception as e:
            print('error main: ')
            print(e)
            continue

    # all_records = upc_database.select_all(table)
    # print(all_records)
    # name_file = "odskek_demo"
    # fieldnames = ['name', 'searched_name', 'searched_upc']
    # writeCsvFile_list(name_file, all_records)

    # upc_database = MysqlDatabase()
    # table = 'upc2'
    # with open("odskek.csv", 'r') as csv_file:
    #     reader = list(csv.reader(csv_file))
    #     i = 1
    #     number = len(reader) - 1
    #     for row in reader:
    #         name = row[0].split(',')[0]
    #         print(name)
    #         col = 'name'
    #         # if upc_database.row_existed(table, col, name):
    #         #     print('Row exsited.')
    #         # else:
    #         data = {
    #             'name': name,
    #         }
    #         upc_database.insertRow(table, data)
    #         print('Row inserted.' + name)
    #         print('Row number: ' + str(i))
    #         i = i + 1


