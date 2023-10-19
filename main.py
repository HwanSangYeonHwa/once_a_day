from bs4 import BeautifulSoup
import os
import requests
import json
import datetime

print('bot start\n')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

request = requests.request(
    method='get', url='https://www.kr.playblackdesert.com/ko-KR/Adventure/Guild/GuildProfile?guildName=%ed%99%98%ec%83%81%ec%97%b0%ed%99%94&region=KR')
request.encoding = None
html = request.content
soup = BeautifulSoup(html, 'html.parser')
data = soup.select(
    '#wrap > div > div.container.guild_profile > article > div.box_list_area > ul')[0]

table = data.findAll('a')

today = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
today.strftime('%Y-%m-%d %H:%M:%S')
members = {}
new_list = []
for item in table:
    url = item.get('href')
    name = item.getText()
    members[name] = url
    new_list.append(name)
print(new_list)

with open(os.path.join(BASE_DIR, 'member.json'), 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

if set(new_list) != set(json_data):
    register = []
    for n in new_list:
        if n in json_data['members']:
            json_data['members'].remove(n)
        else:
            register.append(n)
    if json_data['members'] or register:
        new_members = {}
        for m in register:
            new_members.update({m:members[m]})
        json_data['update'].update({
            today.strftime('%Y-%m-%d') : {
                "register": new_members,
                "unregister": json_data['members']}
                })
        json_data['last_update'] = today.strftime('%Y-%m-%d %H:%M:%S')
    json_data['members'] = new_list

with open(os.path.join(BASE_DIR, 'member.json'), 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent='\t')

print('finish\n')
