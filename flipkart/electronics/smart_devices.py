import csv
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")

url_flipkart = "https://www.flipkart.com"
query_smart_devices = "/search?sid=ajy&otracker=CLP_Filters"
query_brand = "&p%5B%5D=facets.brand%255B%255D%3D"
query_page = "&page="
category = "smart_devices"

def getUniqueID():
    id = 0
    for char in category:
        id+=ord(char)
    return id

def getSmartDeviceBrands():
    brands = []
    with open("flipkart_brands_smart_devices.txt", "r") as infile:
        for brand in infile:
            brands.append(brand.replace("\n", ""))
        infile.close()
    return brands

def getPageLimit(brand):
    url = url_flipkart + query_smart_devices + query_brand + brand
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    page_limit = 1
    try:
        divs = soup.findAll('div', attrs = {'class', '_2zg3yZ'})
        spans = divs[-1].findAll('span')
        page_limit = int(spans[0].text.split(" ")[-1])
    except:
        page_limit = 1
    if page_limit < 50:
        return page_limit
    return 50

def getSmartDevices():
    count = 0
    smart_devices = []
    uniqueID = getUniqueID()
    brands = getSmartDeviceBrands()
    csvfile = open("flipkart_smart_devices.csv", "w")
    jsonfile = open("flipkart_smart_devices.json", "w")
    for brand in brands:
        page_limit = getPageLimit(brand)
        for page in range(1, page_limit+1):
            url = url_flipkart + query_smart_devices + query_brand + brand + query_page + str(page)
            driver.get(url)
            for element in driver.find_elements_by_class_name('_3liAhj'):
                driver.execute_script("arguments[0].scrollIntoView();", element)   
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            divs = soup.findAll('div', attrs = {'class': '_3liAhj'})
            for div in divs:
                count += 1
                try:
                    id = uniqueID + count
                    title = str(div.find('a', attrs = {'class': '_2cLu-l'}).text)
                    price = int(div.find('div', attrs = {'class': '_1vC4OE'}).text.replace('₹', '').replace(',', ''))
                    image = str(div.find('img', attrs = {'alt': title}).get('src'))
                    smart_device = {
                        "id": id,
                        "brand": brand,
                        "title": title,
                        "price": price,
                        "image": image
                    }
                    print(title)
                    smart_devices.append(smart_device)
                    entry = [id, brand, title, price, image]
                    csv.writer(csvfile, lineterminator = '\n').writerow(entry)
                except:
                    continue
    json.dump({"records": smart_devices}, jsonfile)

getSmartDevices()
