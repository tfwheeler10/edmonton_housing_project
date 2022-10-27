import requests
import pandas as pd
import numpy as np
import os
import gspread
import df2gspread as d2g
import warnings
from bs4 import BeautifulSoup
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import geopandas

baseurl = 'https://www.remax.ca/ab/edmonton-real-estate?pageNumber=1'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

productlinks = []
for x in range(1,170):
    r = requests.get(f'https://www.remax.ca/ab/edmonton-real-estate?pageNumber={x}')
    soup = BeautifulSoup(r.content, 'lxml')

    productlist = soup.find_all('div', class_='listing-card_root__UG576 search-gallery_galleryCardRoot__7HbLb')

    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(link['href'])
            
print(productlinks)

df = pd.DataFrame(productlinks)

## testlink = 'https://www.remax.ca/ab/edmonton-real-estate/6115-carr-rd-nw-wp_idm73000004-24973507-lst'

finallist = []
for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    price = soup.find('div', class_='listing-summary_listPrice__PJawt').text.strip()
    address1 = soup.find('span', class_='listing-address_splitLines__pLZIy').text.strip()
    address2 = soup.find('span', class_='listing-summary_cityLine__YxXgL listing-address_splitLines__pLZIy').text.strip()
    listings = {
        'address line 1': address1,
        'address line 2': address2,
        'price': price
    }
    
    finallist.append(listings)
    
df3 = pd.DataFrame(finallist)
print(df3.head(15))

df3.to_csv('remax-listing-exports.csv')

df.to_csv('links.csv')
