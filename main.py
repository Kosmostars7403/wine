from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections

WINERY_CREATION_YEAR = 1920

if __name__ == '__main__':
    today_year = (datetime.date.today()).year
    age_of_winery = today_year - WINERY_CREATION_YEAR

    wines_excel_data_df = pandas.read_excel('wine3.xlsx')
    drinks = wines_excel_data_df.to_dict(orient = 'records')

    sorted_drinks = collections.defaultdict(list)
    for drink in drinks:
        sorted_drinks[drink['Категория']].append(drink)
    pprint(sorted_drinks)


    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age = 'Уже {} лет с вами'.format(age_of_winery),
        white_wines = sorted_drinks['Белые вина'],
        red_wines = sorted_drinks['Красные вина'],
        drinks = sorted_drinks['Напитки']
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)



    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
