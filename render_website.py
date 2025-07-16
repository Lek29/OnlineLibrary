import argparse
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


DEFAULT_DATA_FILE = 'meta_data.json'

def parse_args():
    parser = argparse.ArgumentParser(description='Сгенирировать данные из json файла')
    parser.add_argument(
        '--data-file',
        type=str,
        default=None,
        help='Путь к json файлу'
    )
    return parser.parse_args()

def on_reload(data_file_path):

    with open(data_file_path, 'r', encoding='utf-8') as f:
        books = json.load(f)

    books_per_page = 10
    books_per_row = 2
    all_books_chunks = list(chunked(books, books_per_page))
    total_pages = len(all_books_chunks)

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html']),
        cache_size=0
    )
    template = env.get_template('template.html')

    for page_num, page_books in enumerate(all_books_chunks, 1):
        books_chunks_for_template = list(chunked(page_books, books_per_row))


        output_filepath = 'index.html' if page_num == 1 else f'page{page_num}.html'


        html = template.render(
            books_chunks=books_chunks_for_template,
            total_pages=total_pages,
            current_page=page_num
        )

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(html)


if __name__ == '__main__':
    args = parse_args()

    data_file_path = args.data_file or DEFAULT_DATA_FILE

    on_reload(data_file_path)

    server = Server()
    server.watch('templates/template.html', lambda: on_reload(data_file_path))
    server.watch(data_file_path, lambda: on_reload(data_file_path))
    server.serve(root='.', port=5500, liveport=35729)
