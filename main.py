from bs4 import BeautifulSoup
import os
import requests
import json
import datetime

print('get event bot start\n')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

request = requests.request(method='get', url='https://www.kr.playblackdesert.com/ko-KR/Adventure/Guild/GuildProfile?guildName=%ed%99%98%ec%83%81%ec%97%b0%ed%99%94&region=KR')
request.encoding = None
html = request.content
soup = BeautifulSoup(html, 'html.parser')
data = soup.select('#wrap > div > div.container.guild_profile > article > div.box_list_area > ul')

print(data)

data = soup.select('#wrap > div > div > article > div.tab_container > div > div.event_area > div.event_list')[0]
table = data.findAll('li')

today = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
events = {'events': [], 'last_update': today.strftime('%Y-%m-%d %H:%M:%S')}
for event in table:
    title = event.find_next('strong').find_next('em').getText().split(' (최종 수정')[0].strip()
    count = event.find_next('span', {'class': 'count'}).getText().replace("  ", " ").strip()
    if count == "상시":
        deadline = "-"
    else:
        deadline = (today + datetime.timedelta(days=int(count.split(' ')[0])-1)).strftime('%Y-%m-%d')
    url = event.find_next('a').get('href')
    thumbnail = event.find_next('img').get('src')
    meta = get_meta(url)
    events['events'].append({'title': title, 'deadline': deadline, 'count': count, 'url': url, 'thumbnail': thumbnail, 'meta': meta})

with open(os.path.join(BASE_DIR, 'events.json'), 'w+', encoding='utf-8') as json_file:
    json.dump(events, json_file, ensure_ascii=False, indent='\t')

print('finish\n')
