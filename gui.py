import PySimpleGUI as gui
from utils import get_response, get_title, get_image_links, save_image, create_pdf
from lexicon import resolution_dict

gui.theme('DarkTeal9')

layout = [
    [gui.Text('Введите ссылку книги. Формат ссылки должен быть такой:\n'
              'http://elib.shpl.ru/ru/nodes/11111-some_book#mode/grid/page/1/zoom/1')],
    [gui.Text('Ссылка', size=(25, 1)), gui.InputText(key='link', enable_events=True)],
    [gui.Text('Выберите расширение', size=(25, 1)), gui.Combo(['656 x 883',
                                                               '1146 x 1542',
                                                               '1966 x 2645'],
                                                                key='resolution')],

    [gui.Button('Скачать книгу'), gui.Exit()]
]

window = gui.Window('Скачай книгу!', layout)

while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Скачать книгу':
        zoom = resolution_dict.get(values['resolution'])
        book_link = values['link']
        response = get_response(book_link)
        title = get_title(response)
        image_links = get_image_links(response, zoom=zoom)

        for ind, link in enumerate(image_links):
            save_image(folder=title, name=str(ind + 1), url=link)

        create_pdf(title)

window.close()
