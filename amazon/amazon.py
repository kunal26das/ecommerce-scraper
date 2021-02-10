import requests
from bs4 import BeautifulSoup
import os
import json
import csv

url_amazon = "https://www.amazon.in"
url_common = "/s?rh=n%3A"
cookies = ""

links = {
    "all mobile phones": "1389401031",
    "tablets": "1375458031",
    "wearable devices": "11599648031",
    "laptops": "1375424031",
    "telivisions": "1389396031",
    "headphones": "1388921031",
    "speakers": "1389365031",
    "cameras": "1388977031",
    "gaming": "4092115031",
    "refrigerators": "1380365031",
    "washing machines": "1380369031",
    "household": "1374515031"
}

headers = {
    "Host": "www.amazon.in",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.amazon.in",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "TE": "Trailers"
}

def clearScreen():
    os.system('cls')

def getCookies():
    request = requests.get(url_amazon, headers = headers)
    cookies = request.cookies

def getCategories():
    categories = {}
    url_fetch_categories = "https://www.amazon.in/gp/site-directory"
    request = requests.get(url_fetch_categories)
    soup = BeautifulSoup(request.content, 'html5lib')
    groups = soup.findAll('div', attrs={'class': 'popover-grouping'})
    for group in groups:
        category = group.find('h2', attrs={'class': 'popover-category-name'})
        sub_categories = group.findAll('a', attrs={'class': 'nav_a'})
        categories[category.text] = []
        for sub_category in sub_categories:
            categories[category.text].append(sub_category.text)
    return categories


def getGroceries(target):
    page, count = 2, 0
    url_fetch_grocery = url_amazon+"/s?i=grocery&page="
    with open("groceries.csv", "w") as outfile:
        while (count < target):
            request = requests.get(url_fetch_grocery+str(page), headers = headers, cookies = cookies)
            soup = BeautifulSoup(request.content, 'html5lib')
            divs = soup.findAll('div', attrs = {'class': 'a-section a-spacing-medium'})
            for div in divs:
                if count == target:
                    break
                link = url_amazon + div.find('a', attrs = {'class': 'a-link-normal'}).get('href')
                title = div.find('span', attrs = {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
                brand = getBrand(link)
                price = 0
                try:
                    price = int(div.find('span', attrs = {'class': 'a-price-whole'}).text)
                except:
                    price = 0
                if price == 0:
                    continue
                image = div.find('img', attrs = {'class': 's-image'}).get('src')
                grocery = [title.strip(), brand, price, image]
                csv.writer(outfile, lineterminator = '\n').writerow(grocery)
                clearScreen()
                print("fetching groceries...")
                print("page:", page-1)
                print("progress:", count+1, "/", target)
                print("current:", grocery)
                count += 1
            page += 1

def getProducts(target):
    for category in links:
        page, count = 2, 0
        url_fetch_products = url_amazon + url_common + links[category] + "&page="
        with open(category+".csv", "w") as outfile:
            while count < target:
                request = requests.get(url_fetch_products+str(page), headers = headers, cookies = cookies)
                soup = BeautifulSoup(request.content, 'html5lib')
                divs = soup.findAll('div', attrs = {'class': 'a-section a-spacing-medium'})
                for div in divs:
                    if count == target:
                        break
                    link = url_amazon + div.find('a', attrs = {'class': 'a-link-normal'}).get('href')
                    title = div.find('span', attrs = {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
                    brand = getBrand(link)
                    price = 0
                    try:
                        price = int(div.find('span', attrs = {'class': 'a-price-whole'}).text)
                    except:
                        price = 0
                    if price == 0:
                        continue
                    image = div.find('img', attrs = {'class': 's-image'}).get('src')
                    product = [title.strip(), brand, price, image]
                    csv.writer(outfile, lineterminator = '\n').writerow(product)
                    clearScreen()
                    print("fetching "+category+"...")
                    print("page:", page-1)
                    print("progress:", count+1, "/", target)
                    print("current:", product)
                    count += 1
                page += 1

def getBrand(link):
    request = requests.get(link, headers = headers, cookies = cookies)
    soup = BeautifulSoup(request.content, 'html5lib')
    brand = "null"
    try:
        brand = soup.find('a', attrs = {'id': 'bylineInfo'}).text
    except AttributeError:
        try:
            divs = soup.findAll('div', attrs = {'class': 'a-section a-spacing-none'})
            brand = divs[1].text.replace(" ", "").replace("by", "")
        except:
            brand = "null"
    return brand.strip()

clearScreen()
getCookies()
getProducts(50)
getGroceries(50)
