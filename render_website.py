from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

with open('meta_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')

html = template.render(books=books)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Готово! Откройте index.html")