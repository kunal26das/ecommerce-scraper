import csv
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")

url_flipkart = "https://www.flipkart.com"
query_tablets = "/tablets/pr?sid=tyy%2Chry"
query_brand = "&p[]=facets.brand%255B%255D%3D"
query_page = "&page="
category = "tablets"

def getUniqueID():
    id = 0
    for char in category:
        id+=ord(char)
    return id

def getTabletBrands():
    brands = []
    with open("flipkart_brands_tablets.txt", "r") as infile:
        for brand in infile:
            brands.append(brand.replace("\n", ""))
        infile.close()
    return brands

def getPageLimit(brand):
    url = url_flipkart + query_tablets + query_brand + brand
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

def getTablets():
    count = 0
    tablets = []
    uniqueID = getUniqueID()
    brands = getTabletBrands()
    csvfile = open("flipkart_tablets.csv", "w")
    jsonfile = open("flipkart_tablets.json", "w")
    for brand in brands:
        page_limit = getPageLimit(brand)
        for page in range(1, page_limit+1):
            url = url_flipkart + query_tablets + query_brand + brand + query_page + str(page)
            driver.get(url)
            for element in driver.find_elements_by_class_name('_31qSD5'):
                driver.execute_script("arguments[0].scrollIntoView();", element)   
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            links = soup.findAll('a', attrs = {'class': '_31qSD5'})
            for link in links:
                count += 1
                try:
                    id = uniqueID + count
                    title = str(link.find('div', attrs = {'class': '_3wU53n'}).text)
                    price = int(link.find('div', attrs = {'class': '_1vC4OE _2rQ-NK'}).text.replace('₹', '').replace(',', ''))
                    image = str(link.find('img', attrs = {'alt': title}).get('src'))
                    tablet = {
                        "id": id,
                        "brand": brand,
                        "title": title,
                        "price": price,
                        "image": image
                    }
                    print(title)
                    tablets.append(tablet)
                    entry = [id, brand, title, price, image]
                    csv.writer(csvfile, lineterminator = '\n').writerow(entry)
                except:
                    continue
    json.dump({"records": tablets}, jsonfile)

getTablets()
