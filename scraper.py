from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
import re
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

products_categories = [
    't-shirts-tank-tops',
    'pants',
    'hoodies-sweatshirts',
    'shirts',
    'suits-blazers',
    'cardigans-sweaters',
    'jeans',
    'jackets-coats',
    'shorts',
    'swimwear',
    'sportswear',
    'underwear',
    'socks',
    'accessories',
    'shoes',
    'sleepwear-loungewear',
    'premium-selection',
    'cardigans-sweaters',
    'jackets-coats',
    'knitwear'
]


parent_link = 'https://www2.hm.com/en_us'
additional_link = '?sort=stock&image-size=small&image=model&offset=0&page-size={}'
f = open('./response.json','r')
gender_spec_url = 'men/products'
recommendations = json.load(f)
user_attributes = recommendations['gender_height_bodytype']
category_recommendations = recommendations['cats']['cats']
category_names = list(category_recommendations.keys())
# get the category from the keys
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

products_links = {}


for category in category_names:
    products_links[category] = []
    print(category)
    # create url for this category
    if category in products_categories:
        cat_url = os.path.join(parent_link, gender_spec_url, category+'.html')
        print(cat_url)
        # open this url and get the count of number of items for this product
        driver.get(cat_url)
        time.sleep(0.2)
        # now get the total count of products present in this page
        product_count_element = driver.find_element(By.CLASS_NAME, "filter-pagination")
        product_count_element_text = product_count_element.text
        product_count_str = product_count_element_text.split(' ')[0]
        if product_count_str=='':
            continue
        total_count = int(product_count_str)
        print(total_count)
        
        all_products_url = cat_url+additional_link.format(total_count)
        driver.get(all_products_url)
        element_by_class = driver.find_element(By.CLASS_NAME, "products-listing")
        products_elements = element_by_class.find_elements(By.CLASS_NAME, "product-item")
        for pe in products_elements:
            single_product = driver.find_element(By.CLASS_NAME, "item-link.remove-loading-spinner")
            href = single_product.get_attribute("href")
            title = single_product.get_attribute('title')
            products_links[category].append([title,href])
        



f = open('product_links_men.json','w')
json.dump(products_links, f)
