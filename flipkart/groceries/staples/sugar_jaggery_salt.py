import csv
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")

url_flipkart = "https://www.flipkart.com"
query_groceries = "/grocery/staples/sugar-jaggery-salt/pr?sid=73z,bpe,fdl&marketplace=GROCERY"
query_brand = "&p%5B%5D=facets.brand%255B%255D%3D"
query_page = "&page="
category = "sugar_jaggery_salt"

def getUniqueID():
    id = 0
    for char in category:
        id+=ord(char)
    return id

def getGroceryBrands():
    brands = []
    with open("flipkart_brands_staples_sugar_jaggery_salt.txt", "r") as infile:
        for brand in infile:
            brands.append(brand.replace("\n", ""))
        infile.close()
    return brands

def getPageLimit(brand):
    url = url_flipkart + query_groceries + query_brand + brand
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

def getGroceries():
    count = 0
    groceries = []
    uniqueID = getUniqueID()
    brands = getGroceryBrands()
    csvfile = open("flipkart_brands_staples_sugar_jaggery_salt.csv", "w")
    jsonfile = open("flipkart_brands_staples_sugar_jaggery_salt.json", "w")
    for brand in brands:
        page_limit = getPageLimit(brand)
        for page in range(1, page_limit+1):
            url = url_flipkart + query_groceries + query_brand + brand + query_page + str(page)
            request = requests.get(url)
            driver.get(url)
            for element in driver.find_elements_by_class_name('_3ZexUx'):
                driver.execute_script("arguments[0].scrollIntoView();", element)   
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            divs = soup.findAll('div', attrs = {'class': '_3ZexUx'})
            for div in divs:
                try:
                    id = uniqueID + count
                    title = str(div.find('a').get('title'))
                    measurement = str(div.find('div', attrs = {'class': '_3H3m_4 _3zy0n0'}).text)
                    price = int(div.find('div', attrs = {'class': '_1vC4OE _2DHlR0'}).text.replace('₹', '').replace(',', ''))
                    image = str(div.find('img', attrs = {'alt': title}).get('src'))
                    grocery = {
                        "id": id,
                        "brand": brand,
                        "title": title,
                        "measurement": measurement,
                        "price": price,
                        "image": image
                    }
                    print(title)
                    groceries.append(grocery)
                    entry = [id, brand, title, measurement, price, image]
                    csv.writer(csvfile, lineterminator = '\n').writerow(entry)
                except:
                    continue
    json.dump({"records": groceries}, jsonfile)

getGroceries()
