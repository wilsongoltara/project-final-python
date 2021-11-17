import requests
import datetime
import csv
from PIL import Image
from IPyhton.display import display

def get_datesets(y, labels):
    if type(y) == list:
        database = []
        for i in range(len(y)):
            database.append({
                'label' : labels[i],
                'data' : y[i]
            })
        return database
    else:
        return [{
            'label' : labels[0],
            'data' : y
        }]

def set_title(title=""):
    if title != '':
        display = 'true' 
    else:
        display = 'false'
    return {
        'title': title,
        'display': display
    }

def create_chart(x, y, labels, kind='bar', title=''):
    datasets = get_datesets(y, labels)
    options = set_title(title)
    
    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }
    return chart

def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    response = requests.get(f'{url_base}?c={chart}')
    return response.content

def save_image(path, content):
    with open(path, 'wb', encoding='utf-8') as image:
        image.write(content)

def display_image(path):
    img_pil = Image(path)
    display(img_pil)

URL = 'https://api.covid19api.com/dayone/country/brazil' 
CONFIRMED = 0
DEATHS = 1
RECOVERED = 2
ACTIVE = 3
DATE = 4

response = requests.get(URL)
raw_data = response.json()

final_data = []

for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])

final_data.insert(0,['confirmed', 'Deaths', 'Recovered', 'Active', 'Date'])

for i in range(1, len(final_data)):
    final_data[i][DATE] = final_data[i][DATE][:10]

with open('files/brasil_covid.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

for i in range(1, len(final_data)):
    final_data[i][DATE] = datetime.datetime.strptime(final_data[i][DATE], '%Y-%m-%d')
