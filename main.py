from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse

WINERY_CREATION_YEAR = 1920

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Заполняем витрину магазина ')
    parser.add_argument('file_path', help='Путь в файлу с ассортиментом')
    args = parser.parse_args()
    file_path = args.file_path

    current_year = datetime.date.today().year
    winery_age = current_year - WINERY_CREATION_YEAR

    wines_excel_data_df = pandas.read_excel(file_path).fillna(False)
    drinks = wines_excel_data_df.to_dict(orient = 'records')

    grouped_by_categories_drinks = collections.defaultdict(list)
    for drink in drinks:
        grouped_by_categories_drinks[drink['Категория']].append(drink)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age = 'Уже {} лет с вами'.format(winery_age),
        grouped_by_categories_drinks = grouped_by_categories_drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)



    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
