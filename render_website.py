from tkinter.tix import ListNoteBook

from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os
from livereload import Server
from more_itertools import chunked


def on_reload():
    print('Обнаружено изменение...')

    os.makedirs('pages', exist_ok=True)

    with open('meta_data.json', 'r', encoding='utf-8') as f:
        books = json.load(f)

    book_on_pages = 10
    all_books_chunks = list(chunked(books, book_on_pages))

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html']),
        cache_size=0
    )
    template = env.get_template('template.html')

    for page_num, page_books in enumerate(all_books_chunks, 1):
        books_chunks_for_template = list(chunked(page_books, 2))

        if page_num == 1:
            output_filename = 'index.html'
        else:
            output_filename = f'index{page_num}.html'

        output_filepath = os.path.join('pages', output_filename)


        html = template.render(books_chunks=books_chunks_for_template)

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(html)

    print("Готово! Все страницы с книгами обновлены")

if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('templates/template.html', on_reload)
    server.watch('meta_data.json', on_reload)
    server.serve(root='.', port=5500, liveport=35729)
