from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server

def on_reload():
    print('Обнаружено изменение...')

    with open('meta_data.json', 'r', encoding='utf-8') as f:
        books = json.load(f)

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html']),
        cache_size=0
    )
    template = env.get_template('template.html')

    html = template.render(books=books)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Готово! Обновлён index.html")

if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('templates/template.html', on_reload)
    server.watch('meta_data.json', on_reload)
    server.serve(root='.', port=5500, liveport=35729)
