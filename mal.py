from bs4 import BeautifulSoup
import ast, re, requests
import pandas as pd
# library to generate user agent
from user_agent import generate_user_agent
# generate a user agent
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.63 Safari/537.36'}
page_link ='https://myanimelist.net/animelist/xzeqtr?status=2'
# fetch the content from url
try:
    page_response = requests.get(page_link, timeout=5, headers=headers)
    if page_response.status_code == 200:
        # parse html
        page_content = BeautifulSoup(page_response.content, 'html.parser')
    else:
        print(page_response.status_code)
        # notify, try again
except requests.Timeout as e:
    print("It is time to timeout")
    print(str(e))

tables = page_content.find_all('table',{'class':'list-table'})
table_items = re.findall(r'data-items=.*>', str(tables[0]).replace('&quot;', '"').replace('\\', ''))
# list_final = list(str(table_items[0])[14:-4].split('},{'))
list_final = list(str(table_items[0])[14:-4].split('},{'))

def addbr(inp):
    return str('{' + inp + '}').replace('true', 'True').replace('false', 'False').replace('null', ' None')

dict_list = list(map(ast.literal_eval, list(map(addbr,list_final))))
df = pd.DataFrame(dict_list)
finaldf = df.drop(['status', 'tags', 'anime_id', 'is_rewatching', 'num_watched_episodes', \
                'anime_studios', 'anime_licensors', 'anime_season', 'anime_airing_status', \
                'has_episode_video', 'has_promotion_video', 'has_video', 'video_url', \
                'is_added_to_list', 'start_date_string', 'finish_date_string',\
                'anime_start_date_string', 'anime_end_date_string', 'days_string',\
                'storage_string', 'priority_string'], axis=1)
finaldf.columns = ['Score', 'Title', 'Episodes', 'url', 'image_path', 'type', 'mpaa_rating']