# 使い回し関数とか、クラスに直接いれたくないやつをいれとく
# 基本的には文字列操作とかもこっちにいれてしまいたい

import json
import requests
import re
import sys
import csv
import gspread
import json
import oauth2client.client
from typing import Any
from time import sleep

def make_publisher_dict(publisher_list):
    url_format = "https://ci.nii.ac.jp/books/opensearch/search?publisher={publisher}&year_from=2018&q=&format=json"
    url_dict = {publisher: url_format.format(publisher=publisher) for publisher in publisher_list}
    return url_dict


def fetch_and_convert_json_to_dict(url):
    response = requests.get(url)
    json_dictionary = json.loads(response.text)
    return json_dictionary

def get_title_from_dict(json_dict):
    title = json_dict['@graph'][0]['dc:title'][0]['@value']
    return title

def modify_title_data(title):
    if '書評' in title:
        title_complete = title.replace('書評', '*')
    else:
        title_complete = title
    return title_complete

def get_published_year_month(json_dict):
    date = json_dict['@graph'][0]['prism:publicationDate']
    return date

def modify_published_year_month(date):
    if '-' in date:
        splited_date = date.split('-')
        year = splited_date[0]
        year = year.replace('20', '')
        month = splited_date[1]
    else:
        year = date
        month = '---'
    date_complete = f'{year}-{month}'
    return date_complete

def get_authors(json_dict):
    author = json_dict['@graph'][0]
    if 'dc:creator' in author.keys():
        authors = author['dc:creator'][0][0]['@value']
    else:
        authors = '------'
    return authors

def modify_author_data(author_data):
    if 'dc:creator' in author_data.keys():
        author_data = author_data['dc:creator']
        if "," in author_data:
            author_data = author_data.replace(', ', '・')
        else:
            pass
        if '著' in author_data:
            author_data = author_data.replace('著', '')
        else:
            pass
    else:
        return ""
    return author_data

def get_journal_title(json_dict):
    j_title = json_dict['@graph'][0]['prism:publicationName'][0]['@value']
    return j_title

def modify_journal_title(j_title):
    if '=' in j_title:
        split_j_title = j_title.split('=')
        j_title_complete = split_j_title[0]
    else:
        j_title_complete = j_title
    return j_title_complete

def get_article_volume(json_dict):
    raw_volume = json_dict['@graph'][0]
    if 'prism:number' in raw_volume.keys():
        volume = raw_volume['prism:number']
    else:
        volume = '------'
    return volume

def get_start_page(json_dict):
    raw_startingpage = json_dict['@graph'][0]
    if 'prism:startingPage' in raw_startingpage.keys():
        startingpage = raw_startingpage['prism:startingPage']
    else:
        startingpage = '------'
    return startingpage

def get_end_page(json_dict):
    raw_endingpage = json_dict['@graph'][0]
    if 'prism:endingPage' in raw_endingpage.keys():
        endingpage = raw_endingpage['prism:endingPage']
    else:
        endingpage = '------'
    return endingpage

def fetch_and_convert_json_to_dict(url):
    response = requests.get(url)
    json_dictionary = json.loads(response.text)
    return json_dictionary

def get_urls_from_json_dict(jd):
    urls = []
    articles = jd['@graph'][0]
    if 'items' in articles.keys():
        dictionary_in_list = articles['items']
        # dictionary_in_listはリスト型
        for dictionary in dictionary_in_list:
            article_url = dictionary['rdfs:seeAlso']['@id']
            urls.append(article_url)
    else:
        pass
    return urls

def get_isbn_from_dict(raw_isbn):
    if 'dcterms:hasPart' in raw_isbn.keys():
        raw_isbn = raw_isbn['dcterms:hasPart'][0]['@id']
        isbn_data = raw_isbn.replace('urn:isbn:', '')
        return isbn_data
    else:
        return ""

def isbn_check():
    past_data = open(sys.argv[2], mode='r', encoding='utf-8')
    tsv_reader = csv.reader(past_data, delimiter='\t')
    repetition_count = 0
    isbn = get_isbn_from_dict(raw_isbn)
    for row in tsv_reader:
        past_isbn = row[13]
        if isbn == past_isbn:
            repetition_count += 1
        else:
            pass
    past_data.close()
    if repetition_count == 0:
        return repetition_count
    else:
        pass
