import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    print('Обнаружено изменение...')

    with open('meta_data.json', 'r', encoding='utf-8') as f:
        books = json.load(f)

    print(f"Загружено книг из meta_data.json: {len(books)}")

    books_per_page = 10
    all_books_chunks = list(chunked(books, books_per_page))
    total_pages = len(all_books_chunks)

    print(f"Всего чанков (страниц): {total_pages}")

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html']),
        cache_size=0
    )
    template = env.get_template('template.html')

    for page_num, page_books in enumerate(all_books_chunks, 1):
        books_chunks_for_template = list(chunked(page_books, 2))

        if page_num == 1:
            output_filepath = 'index.html'
        else:
            output_filepath = f'page{page_num}.html'

        html = template.render(
            books_chunks=books_chunks_for_template,
            total_pages=total_pages,
            current_page=page_num
        )

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  Сгенерирован {output_filepath}")

    print("Все страницы с книгами обновлены!")


if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('templates/template.html', on_reload)
    server.watch('meta_data.json', on_reload)
    server.serve(root='.', port=5500, liveport=35729)
