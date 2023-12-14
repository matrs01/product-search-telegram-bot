from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable
from selenium.webdriver.chrome.options import Options


from .item import Item


__all__ = ['Shop', 'Wildberries', 'MVideo']


class Shop(metaclass=ABCMeta):

    '''
    Class for parsing online shops.
    get_html returns html of page with results of searching for query
    parse_items returns list of 'num' (default 5) first items
    '''

    @abstractmethod
    def get_html(query: str):
        pass

    @abstractmethod
    def parse_items(query: str, num=5):
        pass


class Wildberries(Shop):
    '''Implementation of Shop for Wildberries'''

    ref = 'https://www.wildberries.ru/'

    @staticmethod
    def get_html(query: str):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(Wildberries.ref)

        wait = WebDriverWait(driver, timeout=10)
        content_present = presence_of_element_located(
            (By.CLASS_NAME, 'main-page'))
        wait.until(content_present)

        search = driver.find_element(
            by=By.ID,
            value='searchInput',
        )
        search.click()
        search.send_keys(query)
        search.send_keys(Keys.ENTER)

        product_cards_present = presence_of_element_located(
            (By.CLASS_NAME, 'product-card-list'))
        wait.until(product_cards_present)

        html_res = BeautifulSoup(driver.page_source, features="html.parser")
        driver.close()

        return html_res

    @staticmethod
    def parse_items(query: str, num=5):
        html_res = Wildberries.get_html(query)

        goods = html_res.find_all('article')[:num]

        item_list = []
        for good in goods:
            item_ref = good.div.a.get('href').strip()

            img_info = good.find('img')
            img = img_info.get('src').strip()

            price_info = good.find('ins', {'class': 'price__lower-price'})
            price = price_info.text.strip()

            name = good.find(
                'span', {'class': 'product-card__name'}).text.replace('/', '').strip()

            item_list.append(Item(name, price, item_ref, img))

        return item_list


class MVideo(Shop):
    '''Implementation of Shop for MVideo'''

    ref = 'https://www.mvideo.ru/'

    @staticmethod
    def get_html(query: str):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(MVideo.ref)

        wait = WebDriverWait(driver, timeout=10)
        page_loaded = element_to_be_clickable(
            (By.TAG_NAME, 'input'))
        wait.until(page_loaded)

        search = driver.find_element(
            by=By.TAG_NAME,
            value='input',
        )
        search.click()
        search.send_keys(query)
        search.send_keys(Keys.ENTER)

        product_cards_present = presence_of_element_located(
            (By.TAG_NAME, 'mvid-plp-product-cards-layout'))
        wait.until(product_cards_present)

        html_res = BeautifulSoup(driver.page_source, features="html.parser")
        driver.close()

        return html_res

    @staticmethod
    def parse_items(query: str, num=5):
        html_res = MVideo.get_html(query)
        print(len(html_res))
        rows = html_res.find_all(
            'div', {'class': 'product-cards-row ng-star-inserted'})
        print(rows[0])

        names = []
        prices = []
        pics = []
        refs = []
        for row in rows:
            names_info = row.find_all_next(
                'div', {'class': 'product-title product-title--grid'})

            for i in names_info:
                names.append(i.a.text.strip())

            prices_info = row.find_all_next(
                'span', {'class': 'price__main-value'})

            for i in prices_info:
                prices.append(i.text.strip().replace(u'\xa0', u' '))

            pic_ref_info = row.find_all_next(
                'a', {'class': 'product-picture-link'})

            for i in pic_ref_info:
                refs.append('https://www.mvideo.ru' + i.get('href'))
                pics.append('https:' + i.picture.source.get('srcset'))

        item_list = []
        for i in range(min(num, len(names))):
            item_list.append(Item(names[i], prices[i], refs[i], pics[i]))

        return item_list
