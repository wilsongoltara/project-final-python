import requests as req
import datetime as dt
import csv

URL = 'https://api.covid19api.com/dayone/country/brazil' 
CONFIRMED = 0
DEATHS = 1
RECOVERED = 2
ACTIVE = 3
DATE = 4

resp = req.get(URL)
raw_data = resp.json()

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
    final_data[i][DATE] = dt.datetime.strptime(final_data[i][DATE], '%Y-%m-%d')
