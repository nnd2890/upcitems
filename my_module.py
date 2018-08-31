import unicodecsv as csv
from urllib.parse import urlparse
import re
import sys, os
import json

def get_string(parser, XPATH):
    arr = parser.xpath(XPATH)
    str = ''.join(arr).strip() if arr else None
    return str

def get_number(parser, XPATH):
    arr = parser.xpath(XPATH)
    str = ''.join(arr).strip() if arr else None
    number = re.findall(r'\d+[,.]?\d+', str)[0] if str else None
    return number

def is_absolute_url(url):
    return bool(urlparse(url).netloc)

def writeCsvFile(name_file, fieldnames, scraped_data):
    print("Writing scraped data to %s.csv" % name_file)
    with open('%s.csv' % name_file, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for datas in scraped_data:
            if datas:
                for data in datas:
                    writer.writerow(data)
    print("Writing %s.csv Finished!" % name_file)

def writeCsvFile_list(name_file, scraped_data):
    print("Writing scraped data to %s.csv" % name_file)
    with open('%s.csv' % name_file, 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for datas in scraped_data:
            writer.writerow(datas)
    print("Writing %s.csv Finished!" % name_file)


def writeJsonFile(name_file, scraped_data):
    print("Writing scraped data to %s.json" % name_file)
    with open('%s.json' % name_file, 'w') as jsonfile:
        jsonData = []
        for datas in scraped_data:
            if datas:
                for data in datas:
                    jsonData.append(data)
        json.dump(jsonData, jsonfile, indent=4)
    print("Writing %s.json Finished!" % name_file)