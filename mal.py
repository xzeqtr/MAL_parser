from bs4 import BeautifulSoup
import re
import sys
import requests
import pandas as pd
# library to generate user agent
from user_agent import generate_user_agent
# generate a user agent
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.63 Safari/537.36'}

try:
    username = sys.argv[1]
except:
    print('Invalid argument')
    sys.exit()

page_link =f'https://myanimelist.net/animelist/{username}?status=2'
# fetch the content from url
try:
    page_response = requests.get(page_link, timeout=5, headers=headers)
    if page_response.status_code == 200:
        # parse html
        page_content = BeautifulSoup(page_response.content, 'html.parser')
    else:
        print(page_response.status_code)
        sys.exit()
        # notify, try again
except requests.Timeout as e:
    print("It is time to timeout")
    print(str(e))

tables = page_content.find_all('table',{'class':'list-table'})
table_items = re.findall(r'data-items="(\[.*\])">', str(tables[0])\
                    .replace('\\&quot;', "'")\
                    .replace('&quot;', '"'))

df = pd.read_json(table_items[0])

finaldf = df.drop(['status', 'created_at', 'updated_at', 'tags', 'anime_id', 'is_rewatching', 'num_watched_episodes', \
                'anime_studios', 'anime_licensors', 'anime_season', 'anime_airing_status', \
                'has_episode_video', 'has_promotion_video', 'has_video', 'video_url', \
                'is_added_to_list', 'start_date_string', 'finish_date_string',\
                'anime_start_date_string', 'anime_end_date_string', 'days_string',\
                'storage_string', 'priority_string', 'notes', 'editable_notes', 'title_localized',\
                'anime_title_eng', 'anime_total_members', 'anime_total_scores',\
                'demographics'], axis=1)
# finaldf.columns = ['Score', 'Title', 'Episodes', 'url', 'image_path', 'type', 'mpaa_rating']
finaldf.to_csv('mal.csv', sep=';', encoding='utf-8')
