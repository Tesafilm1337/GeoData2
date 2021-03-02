import csv
from datetime import date

import requests
from bs4 import BeautifulSoup
episodes = []
keymap = set()


print('Requesting page...')
html = requests.get("https://www.fernsehserien.de/tatort/sendetermine").text
print('Request successful')

print('Parsing...')
soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('table', {'class': 'sendetermine-2019'})
for table in tables:
    for row in table.find_all('tr'):
        number = next(row.find('td', {'class': 'sendetermine-2019-staffel-und-episode'}).children).text
        title = next(row.find('td', {'class': 'sendetermine-2019-episodentitel'}).children).text
        if not number.isdigit():
            continue
        number = int(number)
        if not number or not title:
            continue
        if number in keymap:
            continue
        keymap.add(number)
        episodes.append({'episode_number': number, 'episode_title': title})
episodes.sort(key=lambda x: x['episode_number'])

with open('episodes-%s.csv' % date.today().strftime("%d.%m.%Y"), mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, ['episode_number', 'episode_title'], dialect=csv.excel)

    writer.writeheader()
    writer.writerows(episodes)

