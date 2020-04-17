#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from time import sleep
from datetime import date,datetime
import lxml
import re

def user_ans(in_name, default):
    print("E.g.: {default[1]}")
    user_input = input(f"{in_name.replace('_',' ').title()}: '.rjust(21,'░'))
    if user_input == '': ## all defaults are already '' .. this if statement is redundant and can be removed, will keep it tho.
        user_ans = default[0]
    else:
        pass
        try: ## Removed some functionality to detect input type and raise error. can be useful for other projects.
            user_ans = user_input ## replace with: user_ans = in_type(user_input)  for type check functionality.
        except:
            print(f'TypeError: Please Enter a valid {in_name}\nE.g.: {default[1]}')  ## Of Type {in_type(default[1])}
    return user_ans

def user_ans_dict(defaults_dict):

    query_dict = {}

    for key, value in defaults_dict.items():
        query_dict[key] = user_ans(key, value) ## To enable type check, add: user_ans(key, type(value[1]), value)
    
    server_query_dict = {    #rules for all answers to fit the query syntax requirements (differs from site to site)
    'title':        re.sub(r'\s','+', query_dict['title']),  ## name must be 'the+godfather'  \s => +
    'title_type':   re.sub(r'\s','_', query_dict['title_type']).lower(),
    'release_date': re.sub(r'\s','', query_dict['release_date']).split(','),
    'user_rating':  re.sub(r'\s','', query_dict['user_rating']).split(','),
    'genres':       re.sub(r'\s','', query_dict['genres']).lower(),
    'certificates': re.sub(r'\s','', query_dict['certificates']).upper().split(','),
    'countries':    re.sub(r'\s','', query_dict['countries']).lower(),
    'languages':    re.sub(r'\s','', query_dict['languages']).lower(),
    'adult':        re.sub(r'\s','', query_dict['adult']).lower(),
    'sort':         re.sub(r'\s','', query_dict['sort']).lower()
    }
    try:
        for i in range(len(server_query_dict['certificates'])):
            server_query_dict['certificates'][i] = 'US%3A' + server_query_dict['certificates'][i]
        server_query_dict['certificates'] = ','.join(server_query_dict['certificates'])
        server_query_dict['release_date'] = f"{date(int(server_query_dict['release_date'][0]),1,1)},{date(int(server_query_dict['release_date'][1]),12,31)}"
        server_query_dict['user_rating'] = f"{round(float(server_query_dict['user_rating'][0]),1)},{round(float(server_query_dict['user_rating'][1]),1)}"
    except:
        for key, value in query_dict.items():
            if value == '':
                server_query_dict[key] = defaults_dict[key][0]
            else:
                pass
    print('11 - Corrected all answers...')
    return server_query_dict

def imdb_search(query_dic,items,per_page):
    "takes query as input - outputs list of URLs for multiple result pages for this query"
    url_list = []
    query_str = ''
    for key in query_dic:
        if query_dic[key] != '':
            query_str += ( key + '=' + str( query_dic[key] ) + '&' )
        else:
            pass
    url = 'https://www.imdb.com/search/title/?' + query_str
    
    if items >= per_page > 0:
        start = [ i for i in range(1,items+1,per_page) ]
        count = [per_page for i in start]
        if items%per_page == 0:
            pass
        else:
            count[-1] = items%per_page
    elif 0 < items < per_page:
        start = [1]
        count = [items]
    else:
        print('00 - Error: Number of Items and PageCount must be positive integers.')
        raise ValueError
    for i in range(len(start)):
        url_list.append( url + f'count={count[i]}&start={start[i]}&ref_=adv_nxt')
    #del query_dic, query_str, url, start, count
    return url_list

def page_title(soup):
    title = soup.find('title')
    return title.text

def download_htmls(urls, html_filename='Untitiled-page', wait_time=10, wait_counter=1, timeout=0.3):
    """Takes a list of URLs, file name, and downloads html files of them.
    Custom headers are disabled by default"""
    # custom headers causes slightly bigger files
    head = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36','Accept':'text/html','Accept-Charset':'utf-8','Accept-Language':'en-US'}
    for n, link in enumerate(urls):
        try:
            print('11 - Connected: Grabbing data...')
            req = requests.get(link, timeout=timeout, headers=head) # custom headers go here: requsts.get( headers=head )
            print(f'11 - Took {req.elapsed} to load')
            req.encoding = 'ISO-8859-1'
            soup = BeautifulSoup(req.text, 'lxml')
            print('11 - Finished parsing page...')
            #pg_title = page_title(soup) #can add page title to the filename
            with open(f'htmls/{html_filename}-{n}.html','w') as web_file:
                web_file.write(str(soup)) #must pass a string while writing
            print(f'11 - Page saved successfully at ~/htmls/{html_filename}-{n}.html')
            d = True
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            print('00 - Error: Loading Timed out....')
            d = False
        if len(urls) > 1:
            for passed in range(0, wait_time, wait_counter):
                print(f'-- - Waiting... T-{str(wait_time-passed).zfill(3)} Sec')
                sleep(wait_counter)
        else:
            pass
    print('11 - Downloaded...')
    return d

def param_ans(in_name, default):
    print(f"Enter {in_name.replace('_',' ').title()}:\nE.g.: {str(default)}")
    user_input = input(': '.rjust(21,'░'))
    if user_input == '': ## all defaults are already '' .. this if statement is redundant and can be removed, will keep it tho.
        user_input = default
    else:
        try: ## Removed some functionality to detect input type and raise error. can be useful for other projects.
            user_input = type(default)(user_input) ## replace with: user_ans = in_type(user_input)  for type check functionality.
        except:
            print(f'TypeError: Please Enter a valid {in_name}\nE.g.: {default}')  ## Of Type {in_type(default[1])}
            exit()
    return user_input

defaults_dict = {                         ## Every dict value contains: key : [default, example]
    'title':        ['','The Dark Knight'],  ## name must be 'the+godfather'  \s => +
    'title_type':   ['','feature, TV series, Documentary,..'],  ##tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,documentary,video_game,short,video,tv_short
    'release_date': ['','(range) - 1995, 2020 or 2000 , 2000'],
    'user_rating':  ['','(range) - 6.5 , 10'],
    'genres':       ['','horror, crime, comedy,..'],
    'certificates': ['','G, PG, PG-13, R, TV-14, TV-MA'], ## must add US%3A before every rating -- HTML encoding: means US:
    'countries':    ['','us,uk,fr,..'],
    'languages':    ['','en,fr,es,de,..'],
    'adult':        ['','include - skip=exclude'],
    'sort':         ['','boxoffice_gross_us,desc - skip=popularity'] ## moviemeter,desc (least popular)
    }

main_params = {
    'items':100,
    'per_page':50,
    'html_filename':'Popular-Drama',
    'csv_filename':'Popular-Drama',
    'wait_time': 10,
    'wait_counter':1,
    'timeout':3,
    'csv_mode':'a'
    }

for key, value in main_params.items():
    main_params[key] = param_ans(key, value)
query_dic = user_ans_dict(defaults_dict)
urls = imdb_search(query_dic,main_params['items'], main_params['per_page'])
files = [ [ i, f"{main_params['html_filename']}-{i}.html", f"{main_params['csv_filename']}-{i}.csv"] for i in range(len(urls)) ]
