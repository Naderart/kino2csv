#!/usr/bin/python3

def welcome():
    w = 42
    frame = f"""\n{'▲'*w}\n{'·'*w}\n{' Welcome to Kino 0.2.0 '.center(w,'·')}\n{' A Movie/TV Data Scrapper '.center(w,'·')}\n{' @naderart - 2020 '.center(w,'·')}\n{'·'*w}\n{'▼'*w}""".splitlines()
    text = """\nKino helps you gather thousands of\nFilm/show data, updated in real-time\nand saved as csv files\nToo many input prompts? No problemo\nSkip by hitting 'Enter'\nEnjoy!""".splitlines()
    sleep(0.5)
    for i in frame:
        print(i)
        sleep(0.03)
    sleep(1)
    for i in text:
        print(i.center(w,' '))
        sleep(0.03)
    sleep(1)

def main(main_params):
    if path.exists('csv'):
        pass
    else:
        mkdir('csv')
    #failed = []
    try:
        for n, url in enumerate(urls):
            soup = download_html(url,main_params['timeout'])
            if soup == 0:
                print(f'Error.. page{n} - soup = 0')
                #failed.append(urls[n])
            else:
                structured_Data = soup_extract(soup)
                print(f'11 - Structured data')
                csv_out(n, structured_Data, main_params['file_name'])
                print(f"11 - Appended data to /csvs/{main_params['file_name']}.csv")
            if n < len(urls)-1:
                for sec in range(0,main_params['wait_time'],main_params['wait_counter']):
                    print( f"-- - Waiting... T-{ str(main_params['wait_time']-sec).zfill( len( str(main_params['wait_time']) ) )} sec" )
                    sleep(main_params['wait_counter'])
            else:
                print( '11 - Finished.')
    except:
        print('00 - Error: Unknown Error...')

from time import sleep

welcome()

from user_input import urls, download_html, main_params
from html_to_csv import soup_extract, csv_out
from os import path, mkdir

if __name__ == "__main__":
    main(main_params)