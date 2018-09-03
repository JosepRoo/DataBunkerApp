from app import Database
from app.models.brands.brand import Brand
from app.models.brands.constants import COLLECTION as BRAND_COLLECTION
from app.models.categories.category import Category
from app.models.channels.channels import Channel
from app.models.logs.log import Log
from app.models.products.product import COLLECTION as PRODUCT_COLLECTION
from app.models.products.product import Product
from app.models.uploads.base_upload import BaseUpload

from bs4 import BeautifulSoup
import datetime
import hashlib
import math
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Walmart(BaseUpload):
    URL = 'https://super.walmart.com.mx/mapa-del-sitio'
    BASE = 'https://super.walmart.com.mx'

    @classmethod
    def build_tree(cls):
        now = datetime.datetime.now()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = './chromedriver_win32/chromedriver.exe'
        browser = webdriver.Chrome(driver, chrome_options=chrome_options)
        browser.set_page_load_timeout(20)
        browser_cats = webdriver.Chrome(driver, chrome_options=chrome_options)
        browser_cats.set_page_load_timeout(20)
        browser_sub_cats = webdriver.Chrome(driver, chrome_options=chrome_options)
        browser_sub_cats.set_page_load_timeout(20)
        browser_products = webdriver.Chrome(driver, chrome_options=chrome_options)
        browser.get(cls.URL)
        links = browser.find_elements_by_class_name("_5I021sOIh5qArdWFNJNOL").copy()
        # del browser
        urls = []
        print(len(links))
        for link in links:
            url = link.get_attribute("href")
            if len(url.split('/')) == 6:
                # urls.append(url)
                browser_cats.get(url)
                time.sleep(0.7)
                soup = BeautifulSoup(browser_cats.page_source, 'lxml')
                all_sub_categories = soup.find_all("div", {"class": "_2lpzO5XrkK7CZfkB8buy21"})
                print("\t", len(all_sub_categories))
                for sub_category in all_sub_categories:
                    sub_category_url = cls.BASE + sub_category.find('a')['href']

                    while True:
                        try:
                            browser_sub_cats.get(sub_category_url)
                        except TimeoutException:
                            # print("Timeout, retrying...")
                            continue
                        else:
                            break
                    try:
                        WebDriverWait(browser_sub_cats, 200).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="root"]/div/div/main/div[1]/section/div[1]/div[2]/div[1]/p')))
                    except TimeoutException:
                        continue
                    pre_soup = browser_sub_cats.page_source.encode("utf")
                    soup = BeautifulSoup(pre_soup, 'lxml')
                    num_items = soup.find("p", {
                        "class": "_34YSfGmQlYtq5kY7JLZ7Ib _2Q77lQio2oYR8Hw1RSqLcu qtJC0387O0QmtTCZiKLCt"}).text.strip().replace(
                        'productos', "")
                    try:
                        pages = math.ceil(int(float(num_items)) / 20)
                    except:
                        pages = 1
                    print("\t\t", num_items)
                    for page in range(0, pages):
                        page_iterator = str(page * 20)
                        product_url = sub_category_url + '?No=' + page_iterator
                        browser_products.get(product_url)
                        time.sleep(0.5)
                        soup = BeautifulSoup(browser_products.page_source, 'lxml')
                        all_products = soup.find_all("div", {"class": "wgFsXe0rWIHJdHC4IodHq"})
                        for item in all_products:
                            d = dict()
                            d['Canal'] = 'Wal-Mart '  # cls.get_channel()
                            d["Date"] = now.strftime("%Y-%m-%d %H:%M")
                            d["Image"] = f"{cls.BASE}{item.find('img')['src']}"
                            d["Item"] = item.find("p",
                                                  {"class": "_34YSfGmQlYtq5kY7JLZ7Ib _3RwjlfvJtz6NfVmm6CO363"}).text
                            d["Price"] = item.find("p", {
                                "class": "_34YSfGmQlYtq5kY7JLZ7Ib qtJC0387O0QmtTCZiKLCt _3URSxitsrGAcwITNRI6nvM"}).text
                            d["Marca"] = (product_url.split("/")[-4]).replace('-', ' ') + ' - ' + (
                                product_url.split("/")[-3]).replace('-', ' ')
                            d["UPC"] = d['Image'].split("/")[-1].replace('m.jpg', '').zfill(16)
                            d["Category"] = product_url.split("/")[-5].replace('-', ' ')
                            urls.append(d)
        browser_cats.close()
        browser.quit()
        return urls
        # response = requests.get(cls.URL)
        # replacers = ["\n", " ", "$", "Equipo", ","]
        # soup = BeautifulSoup(response.text, "html.parser")
        # elements = soup.find_all("div", {"class": "[ row has-hover-bg ] [ pad-y-3 bor-b-1 ]"})
        # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # channel = cls.get_channel()
        # category, upsert = cls.upsert_category(channel._id)
        # if upsert:
        #     category.save_to_mongo(category.get_collection())
        # brands_to_insert = list()
        # products_to_insert = list()
        # length = 0
        # for item in elements:
        #     product = item.find("h4", {"class": "mar-0"}).text.replace("\r\n", "").strip()
        #     price = item.find("div", {"class": "[ col-xs-8 ] [ col-sm-4 ] [ pad-y-3 text-center ]"}).text
        #     for rep in replacers:
        #         price = price.replace(rep, "")
        #     brand = product.split(' ')[0]
        #     brand, insert = cls.upsert_brand(brand, category._id)
        #     if insert:
        #         brands_to_insert.append(brand.json(date_to_string=False))
        #     upc = hashlib.md5(product.encode('utf-8')).hexdigest()[:16]
        #     image = item.find("img")['src']
        #     sub_elements = {'date': now, 'value': float(price)}
        #     product, upsert = cls.upsert_product(upc, channel._id, image=image, sub_elements=sub_elements,
        #                                          product=product)
        #     if upsert:
        #         products_to_insert.append(product.json(date_to_string=False))
        #     length += 1
        # if brands_to_insert:
        #     Database.insert_many(BRAND_COLLECTION, brands_to_insert)
        # if products_to_insert:
        #     Database.insert_many(PRODUCT_COLLECTION, products_to_insert)

    @staticmethod
    def get_channel():
        return Channel.get_by_name("Wal-Mart")

    @staticmethod
    def upsert_category(channel_id):
        # category = Category.get_by_name("Celulares", channel_id)
        # insert = False
        # if category is None:
        #     category = Category("Celulares", channel_id)
        #     insert = True
        # return category, insert
        pass

    @staticmethod
    def upsert_brand(brand_name, category_id):
        # brand = Brand.get_by_name(brand_name, category_id)
        # insert = False
        # if brand is None:
        #     brand = Brand(brand, category_id)
        #     insert = True
        # return brand, insert
        pass

    @staticmethod
    def upsert_product(product_upc, channel_id, **kwargs):
        pass
        # product = Product.get_by_UPC(product_upc, channel_id)
        # insert = False
        # if product is None:
        #     product = Product(product, channel_id, **kwargs)
        #     insert = True
        # elif not product.is_duplicated_date(kwargs['sub_elements']['date']):
        #     product.sub_elements.append(Log(**kwargs['sub_elements']))
        #     product.update_mongo(product.get_collection())
        # return product, insert
