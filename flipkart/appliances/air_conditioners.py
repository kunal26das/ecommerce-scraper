import csv
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")

url_flipkart = "https://www.flipkart.com"
query_air_conditioners = "/air-conditioners/pr?sid=j9e%2Cabm%2Cc54"
query_brand = "&p[]=facets.brand%255B%255D%3D"
query_page = "&page="
category = "air_conditioners"

def getUniqueID():
    id = 0
    for char in category:
        id+=ord(char)
    return id

def getAirConditionerBrands():
    brands = []
    with open("flipkart_brands_air_conditioners.txt", "r") as infile:
        for brand in infile:
            brands.append(brand.replace("\n", ""))
        infile.close()
    return brands

def getPageLimit(brand):
    url = url_flipkart + query_air_conditioners + query_brand + brand
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    page_limit = 1
    try:
        divs = soup.findAll('div', attrs = {'class', '_2zg3yZ'})
        spans = divs[-1].findAll('span')
        page_limit = int(spans[0].text.split(" ")[-1])
    except:
        page_limit = 1
    return page_limit

def getAirConditioners():
    count = 0
    air_conditioners = []
    uniqueID = getUniqueID()
    brands = getAirConditionerBrands()
    csvfile = open("flipkart_air_conditioners.csv", "w")
    jsonfile = open("flipkart_air_conditioners.json", "w")
    for brand in brands:
        page_limit = getPageLimit(brand)
        for page in range(1, page_limit+1):
            url = url_flipkart + query_air_conditioners + query_brand + brand + query_page + str(page)
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
                    air_conditioner = {
                        "id": id,
                        "brand": brand,
                        "title": title,
                        "price": price,
                        "image": image
                    }
                    print(title)
                    entry = [id, brand, title, price, image]
                    air_conditioners.append(air_conditioner)
                    csv.writer(csvfile, lineterminator = '\n').writerow(entry)
                except:
                    continue
    json.dump({"records": air_conditioners}, jsonfile)

getAirConditioners()
