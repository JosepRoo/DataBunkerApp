from app import Database
from app.models.brands.constants import COLLECTION as BRAND_COLLECTION
from app.models.categories.constants import COLLECTION as CATEGORY_COLLECTION
from app.models.products.product import COLLECTION as PRODUCT_COLLECTION
from app.models.uploads.base_upload import BaseUpload

from bs4 import BeautifulSoup
import datetime
import math
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Walmart(BaseUpload):
    URL = 'https://super.walmart.com.mx/mapa-del-sitio'
    BASE = 'https://super.walmart.com.mx'
    now = datetime.datetime.now()
    options = Options()
    options.add_argument("-headless")
    executable_path = './geckodriver-v0.22.0-win64/geckodriver.exe'
    channel_name = 'Wal-Mart'

    @classmethod
    def browse_categories(cls, url, browser_cats, browser_sub_cats, browser_products, now, channel):
        categories_to_insert = list()
        brands_to_insert = list()
        products_to_insert = list()
        prodcuts_updated = 0
        if len(url.split('/')) == 6:
            browser_cats.get(url)
            time.sleep(0.7)
            soup = BeautifulSoup(browser_cats.page_source, 'lxml')
            all_sub_categories = soup.find_all("div", {"class": "_2lpzO5XrkK7CZfkB8buy21"})
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
                    WebDriverWait(browser_sub_cats, 180).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="root"]/div/div/main/div[1]/section/div[1]/div[2]/div[1]/p')))
                except TimeoutException:
                    continue
                url_split = sub_category_url.split("/")
                category, inserted = cls.upsert_category(channel._id, url_split[-5].replace('-', ' '))
                if inserted:
                    categories_to_insert.append(category.json(date_to_string=False))
                brand_name = url_split[-4].replace('-', ' ') + ' - ' + (url_split[-3]).replace('-', ' ')
                brand, inserted = cls.upsert_brand(category._id, brand_name)
                if inserted:
                    brands_to_insert.append(brand.json(date_to_string=False))
                pre_soup = browser_sub_cats.page_source.encode("utf")
                soup = BeautifulSoup(pre_soup, 'lxml')
                num_items = soup.find("p", {
                    "class": "_34YSfGmQlYtq5kY7JLZ7Ib _2Q77lQio2oYR8Hw1RSqLcu qtJC0387O0QmtTCZiKLCt"}).text.strip().replace(
                    'productos', "")
                try:
                    pages = math.ceil(int(float(num_items)) / 20)
                except:
                    pages = 1
                for page in range(pages):
                    page_iterator = str(page * 20)
                    product_url = sub_category_url + '?No=' + page_iterator
                    browser_products.get(product_url)
                    time.sleep(0.8)
                    soup = BeautifulSoup(browser_products.page_source, 'lxml')
                    all_products = soup.find_all("div", {"class": "wgFsXe0rWIHJdHC4IodHq"})
                    for item in all_products:
                        date = now.strftime("%Y-%m-%d %H:%M")
                        image = f"{cls.BASE}{item.find('img')['src']}"
                        product_name = item.find("p",
                                                 {"class": "_34YSfGmQlYtq5kY7JLZ7Ib _3RwjlfvJtz6NfVmm6CO363"}).text
                        price = item.find("p", {
                            "class": "_34YSfGmQlYtq5kY7JLZ7Ib qtJC0387O0QmtTCZiKLCt _3URSxitsrGAcwITNRI6nvM"}).text
                        price = price.replace("$", "")
                        sub_elements = {"date": date, "value": float(price)}
                        upc = image.split("/")[-1].replace('m.jpg', '').zfill(16)
                        product, inserted, updated = cls.upsert_product(upc,
                                                                        channel._id,
                                                                        image=image,
                                                                        name=product_name,
                                                                        sub_elements=sub_elements,
                                                                        parentElementId=brand._id,
                                                                        grandParentId=category._id
                                                                        )
                        if inserted:
                            products_to_insert.append(product.json(date_to_string=False))
                        prodcuts_updated += updated
        if categories_to_insert:
            Database.insert_many(CATEGORY_COLLECTION, categories_to_insert)
        if brands_to_insert:
            Database.insert_many(BRAND_COLLECTION, brands_to_insert)
        if products_to_insert:
            Database.insert_many(PRODUCT_COLLECTION, products_to_insert)
        return len(products_to_insert), prodcuts_updated

    @classmethod
    def build_tree(cls):
        browser = Firefox(executable_path=cls.executable_path, firefox_options=cls.options)
        browser.set_page_load_timeout(20)
        browser_cats = Firefox(executable_path=cls.executable_path, firefox_options=cls.options)
        browser_cats.set_page_load_timeout(20)
        browser_sub_cats = Firefox(executable_path=cls.executable_path, firefox_options=cls.options)
        browser_sub_cats.set_page_load_timeout(20)
        browser_products = Firefox(executable_path=cls.executable_path, firefox_options=cls.options)
        browser.get(cls.URL)
        links = browser.find_elements_by_class_name("_5I021sOIh5qArdWFNJNOL")
        products_inserted = 0
        products_updated = 0
        channel = cls.get_channel(cls.channel_name)
        for link in links:
            url = link.get_attribute("href")
            inserted, updated = cls.browse_categories(url, browser_cats, browser_sub_cats, browser_products, cls.now,
                                                      channel)
            products_inserted += inserted
            products_updated += updated
            break
        browser_cats.close()
        browser_products.close()
        browser_sub_cats.close()
        browser.quit()
        return {"inserted": products_inserted, "updated": products_updated}
