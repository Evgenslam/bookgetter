import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import re
import time


options_chrome = webdriver.ChromeOptions()
#options_chrome.add_argument('--headless')

url = 'http://elib.shpl.ru/ru/nodes/38777#mode/grid/page/1/zoom/1'
my_headers: dict = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}
the_url = 'http://elib.shpl.ru/ru/nodes/38777#mode/grid/page/2/zoom/5'

response = requests.get(url=the_url, headers=my_headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
pattern = re.compile(r'dv-page dv-page-\d+')


# checker = soup.find('div', {'class': 'dv-viewport'})
#
# print(checker)


#[print(x['src'] ) for x in soup.find_all('img')]     #('div', {"class": "translate-input key-en"}))



page_url = "http://elib.shpl.ru/ru/nodes/38777#mode/grid/page/1/zoom/5"

with webdriver.Chrome(options=options_chrome) as browser:
    browser.get(page_url)
    browser.maximize_window()
    full_height = browser.execute_script("return document.body.scrollHeight")
    page_height = browser.execute_script("return window.innerHeight")
    times_to_scroll = full_height//page_height
    for i in range(times_to_scroll):
        browser.execute_script(f"window.scrollTo({i*page_height}, {(i+1) * page_height});")
        time.sleep(2)
    time.sleep(2)
    elements = browser.find_elements(By.CSS_SELECTOR, "[class*='dv-page'][class*='dv-page-']")


    for ind, el in enumerate(elements):
        img_el = el.find_element(By.TAG_NAME, 'img').get_attribute('src')
        image_source = requests.get(img_el, headers=my_headers)
        with open(f'images/{ind+1}.jpg', 'wb') as file:
            file.write(image_source.content)





# def save_image(folder:str, name: str, url:str) -> None:
#     image_source = requests.get(url)
#     output = name + '.png'
#
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     with open(f'{folder}{output}', 'wb') as file:
#         file.write(image_source.content)
#         print(f'Скачался файл: {output}')
#         print(image_source)
#         print()
#         print(image_source.content)
#
# save_image(folder=r'C:\Users\User\Desktop\Kolchak', name='page_2', url=url)
