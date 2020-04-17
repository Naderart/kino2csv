#!/usr/bin/python3

def welcome():
    sleep(0.5)
    width = 42
    print(''.center(width,'▲'))
    sleep(0.04)
    print(''.center(width,'·'))
    sleep(0.04)
    print(' Welcome to Kino 0.2.0 '.center(width,'·'))
    sleep(0.04)
    print(' A Movie/TV Data Scrapper '.center(width,'·'))
    sleep(0.04)
    print(' @naderart - 2020 '.center(width,'·'))
    sleep(0.04)
    print(''.center(width,'·'))
    sleep(0.04)
    print(''.center(width,'▼'))
    sleep(1)
    text = """\nKino helps you gather thousands of\nFilm/show data, updated in real-time\nand saved as csv files\nToo many input prompts? No problemo\nSkip by hitting 'Enter'\nEnjoy!\n """.splitlines()
    for i in text:
        print(i.center(width,' '))
        sleep(0.03)
    sleep(0.5)

def main(main_params):
    try:
        downloaded = download_htmls(urls,html_filename=main_params['html_filename'],wait_time=main_params['wait_time'], wait_counter=main_params['wait_counter'],timeout=main_params['timeout'])
        if downloaded == True: # if downloaded == True
            for i, html, csv in files:
                soup = html_soup(f'htmls/{html}', 'lxml')
                print('11 - Made Soup!')
                structured_Data = soup_extract(soup)
                #print(f'11 - Structured data from /htmls/{html} into Python data')
                print(f'11 - Structured data')  ## simpler terminology for logging
                csv_out(i, structured_Data, f'csvs/{csv}', mode=main_params['csv_mode']) # Multiple CSV files - one for each html
                if main_params['csv_mode'] == 'w':
                    #print(f'11 - Created .CSV file from {html} at ~/csvs/{csv}') # Another approach: append all into one CSV file
                    print(f'11 - Created ~/csvs/{csv}') ## simpler terminology for logging
                else:
                    #print(f"11 - Appended data from file {html} to ~/csvs/{main_params['csv_filename']}-appended.csv")
                    print(f"11 - Appended data to ~/csvs/{main_params['csv_filename']}-append.csv") ## simpler terminology for logging
        else:
            print('00 - Error: Less HTML Files were downloaded than expected...')
    except:
        print('00 - Error: Unknown Error.....')

from time import sleep

welcome()

from user_input import urls, download_htmls, files, main_params
from html_to_csv import html_soup, soup_extract, csv_out

main(main_params)