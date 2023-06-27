import requests
import os
import re
from typing import List
from bs4 import BeautifulSoup
from PIL import Image
from fpdf import fpdf


my_headers: dict = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}


cli_book_link = 'http://elib.shpl.ru/ru/nodes/85429-mirtov-a-v-donskoy-slovar-materialy-k-izucheniyu-leksiki-donskih-kazakov-rostov-na-donu-1929-trudy-severo-kavkazskoy-assotsiatsii-nauchno-issledovatelskih-institutov-locale-nil-58-vyp-6#mode/grid/page/1/zoom/1'


def get_response(book_url: str):
    session = requests.Session()
    session.headers.update(my_headers)
    response = session.get(book_url)
    print(type(response))
    return response


def get_image_links(response, zoom: int) -> List[str]:
    pattern = re.compile('"id":(\d+)')
    ids = re.findall(pattern, response.text)
    image_links = [f'http://elib.shpl.ru/pages/{str(_id)}/zooms/{str(zoom)}' for _id in ids]
    [print(x) for x in image_links]
    return image_links


def get_title(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title = [x for x in soup.find('a', {'class': 'value_of_type_7'}).text if x not in '?*:"<>|/']
    title = ''.join(title)
    return title


def get_image(image_link: str):
    image = requests.get(image_link, headers=my_headers).content
    return image


def save_image(folder: str, name: str, url: str) -> None:
    final_folder = 'C:\\Users\\User\\Desktop\\' + folder
    final_name = name + '.jpg'
    image = get_image(image_link=url)
    if not os.path.exists(final_folder):
        os.makedirs(final_folder)
    with open(f'{final_folder}\\{final_name}', 'wb') as file:
        file.write(image)
        print(f'Скачался файл: {final_name}')


def create_pdf(title: str):
    full_folder = 'C:\\Users\\User\\Desktop\\' + f'{title}\\'
    img_list = sorted(os.listdir(full_folder), key=lambda x: int(x.split('.')[0]))
    image = Image.open(full_folder + img_list[0])
    width, height = image.size
    image.close()

    pdf = fpdf.FPDF(format=(width, height))
    pdf.set_auto_page_break(0)

    for img in img_list:
        pdf.add_page()
        image = full_folder + img
        pdf.image(image, x=0, y=0, w=width, h=height)

    pdf.output(f'{full_folder}'+f'{title}.pdf')
    print('Создан pdf!')





