from bs4 import BeautifulSoup
import re
import csv
from user_input import main_params
import lxml

# director & Stars: maybe find link to dir & stars pages

def html_soup(file_in, parser='lxml'):
    "Opens html file -- return a soup object of whole page."
    with open(file_in,'r') as html_file:
        cache = html_file.read()
        soup = BeautifulSoup(cache, 'lxml') # Do not use prettyfiy() here, turns soup object into string
    return soup

def formulas(i):
    """Template for creating a dictionary for 1 film/show data
    Try / Except : to avoid errors messing up the order of data
    If it can't be extracted, a null value '' is bruteforced
    To be able to reproduce this scrapperr for other sites, make another specific template like this."""
    dict_ = {}
    dict_['Index'] = str(i.h3.span.text).strip('.')
    dict_['Title'] = str(i.h3.a.text)
    dict_['Link'] = f"""https://www.imdb.com{re.search(r'<a href="([A-Za-z0-9/]+)', str(i.h3.a)).group(1)}"""
    try:
        dict_['Year'] = re.search(r'\d{4}', i.h3.find('span', class_='lister-item-year text-muted unbold').text).group(0)
    except:
        dict_['Year'] = ''
    try:
        dict_['Certification'] = i.p.find('span', class_='certificate').text
    except:
        dict_['Certification'] = ''
    try:
        dict_['Runtime'] = i.p.find('span', class_='runtime').text.strip(' min')
    except:
        dict_['Runtime'] = ''
    try:
        dict_['Genres'] = i.find('span',class_='genre').get_text(strip=True)
    except:
        dict_['Genres'] = ''
    try:
        dict_['Rating'] = i.find('div', class_='inline-block ratings-imdb-rating').strong.text
    except:
        dict_['Rating'] = ''
    try:
        dict_['Description'] = i.find('p',class_='').find_previous().get_text(strip=True)
    except:
        dict_['Description'] = ''
    try:
        dict_['Gross'] = i.find_all('span',attrs={'name':'nv'})[1]['data-value']
    except:
        dict_['Gross'] = ''
    try:
        dict_['Director'] = ', '.join([d.text for d in BeautifulSoup(str(i.find('p', class_='')).split('Stars')[0],'lxml').find_all('a')])
    except:
        dict_['Director'] = ''
    try:
        dict_['Stars'] = ', '.join([d.text for d in BeautifulSoup(str(i.find('p', class_='')).split('Stars')[1],'lxml').find_all('a')])
    except:
        dict_['Stars'] = ''
    return dict_

def soup_extract(soup):
    """Takes soup object (page)
    Loops to find a specific html (div) or (class) containing all data needed (data frame)
    Each loop, Applies 'formulas(i)' to data frame -- formulas(i) extracts data into a dictionary -- dict is appendded to a list
    This format makes data ready to conversion to CSV file. List[ dict1{}, dict2{}, ... ]"""
    dicts_in_list = []
    for i in soup.find_all('div', class_='lister-item-content'):
        dicts_in_list.append( dict(formulas(i)) )  # directly append dict to list points in memory to the same value, fix: list.append( dict(dict_) )
    return dicts_in_list

def csv_out1(i, dicts_in_list, file_out, mode='w'):
    """Opens a new CSV file, writes or appends to it."""
    if mode == 'a':
        file_out = f"csvs/{main_params['csv_filename']}-appended.csv"
    else:
        pass
    with open(file_out, mode ) as csv_file:
        try:
            writer = csv.DictWriter(csv_file, fieldnames=list(dicts_in_list[0].keys()))
            if i == 0:
                writer.writeheader()
            elif i > 0 and mode == 'w':
                writer.writeheader()
            else:
                pass
            writer.writerows(dicts_in_list)
        except:
            print('00 - Error: CSV file Could not be created.....')

#soup = html_soup('htmls/IMDb-big-0.html')
#dicts = soup_extract(soup)
#print(dicts[0])
