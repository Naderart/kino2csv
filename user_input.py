#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from time import sleep
from datetime import date,datetime
import lxml
import re

def user_ans(in_name, default, example):
    print(f"\nE.g.: {example}")
    in_name = in_name.replace('_',' ').title()
    ans = False
    while ans is False:
        user_input = input( f"{in_name}".center(21,'░') + ': ' )    
        if user_input == '':
            user_input = default
            ans = True
        else:
            try:
                user_input = type(default)(user_input)
                ans = True
            except:
                print(f'{in_name}={user_input} is not valid. Try again')
                ans = False
    return user_input

def user_ans_dict(defaults_dict):
    query_dict = {}
    for key, value in defaults_dict.items():
        query_dict[key] = user_ans(key, value[0], value[1])
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
            query_str += key + '=' + str( query_dic[key] ) + '&'
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
    for i, start in enumerate(start):
        url_list.append( url + f'count={count[i]}&start={start}&ref_=adv_nxt')
    #del query_dic, query_str, url, start, count
    return url_list

def page_title(soup):
    title = soup.find('title')
    return title.text

def download_html(url, timeout):
    """Takes a list of URLs, file name, and downloads html files of them.
    Custom headers are enabled by default"""
    payload = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
        'Accept':'text/html',
        'Accept-Charset':'utf-8',
        'Accept-Language':'en-US'}
    try:
        print('11 - Connected: Grabbing data...')
        req = requests.get(url, timeout=timeout, headers=payload) # custom headers go here: requsts.get( headers=head )
        print(f'11 - Took {req.elapsed} to load')
        req.encoding = 'ISO-8859-1'
        soup = BeautifulSoup(req.text, 'lxml')
        print('11 - Finished parsing page...')
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        soup = 0
        print('00 - Loading Timed out....')
    return soup


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
    'file_name':'crime',
    'wait_time': 10,
    'wait_counter':1,
    'timeout':10.0
    }

query_dic = user_ans_dict(defaults_dict)

for key, value in main_params.items():
    main_params[key] = user_ans(key, value, value)

urls = imdb_search(query_dic,main_params['items'], main_params['per_page'])