# 使い回し関数とか、クラスに直接いれたくないやつをいれとく
# 基本的には文字列操作とかもこっちにいれてしまいたい

import json
import requests
import re
import sys
import csv
import json
import oauth2client.client
from typing import Any
from time import sleep


def make_publisher_dict(publisher_list):
    url_format = "https://ci.nii.ac.jp/books/opensearch/search?publisher={publisher}&year_from=2018&q=&format=json"
    url_dict = {publisher: url_format.format(publisher=publisher) for publisher in publisher_list}
    return url_dict


def fetch_and_convert_json_to_dict(url):
    response = requests.get(url).text
    json_dictionary = json.loads(response)
    src_list = json_dictionary['@graph'][0]['items']
    return src_list


def get_title_data(src):
    if src.get('dc:title'):
        title = src['dc:title'][0]['@value']
    else:
        title = src.get('title')
    if title:
        if '書評' in title:
            title_complete = title.replace('書評', '*')
        else:
            title_complete = title
    else:
        title_complete = ""
    return title_complete


def get_published_date_data(src):
    date = src.get('prism:publicationDate')
    if date:
        if '-' in date:
            splited_date = date.split('-')
            year = splited_date[0]
            year = year.replace('20', '')
            month = splited_date[1]
        else:
            year = date
            month = '---'
        date_complete = f'{year}-{month}'
    else:
        date_complete = ''
    return date_complete


def get_authors_data(src):
    if src.get('dc:creator') and isinstance(src.get('dc:creator'), list) and len(src.get('dc:creator')) > 0:
        authors_list = src['dc:creator']
        author_array = [author['@value'] for author in authors_list]
    elif src.get('dc:creator'):
        author_array = [src.get('dc:creator')]
    else:
        author_array = []
    authors = '・'.join(author_array)
    if authors and "," in authors:
        authors = authors.replace(', ', '・')
    if authors and '著' in authors:
        authors = authors.replace('著', '')
    return authors


def get_journal_title_data(src):
    if src.get('prism:publicationName'):
        if isinstance(src.get('prism:publicationName'), list):
            j_title = src['prism:publicationName'][0]['@value']
        else:
            j_title = src['prism:publicationName']
    else:
        j_title = ""

    if j_title and '=' in j_title:
        split_j_title = j_title.split('=')
        j_title_complete = split_j_title[0]
    else:
        j_title_complete = j_title
    return j_title_complete


def get_article_volume(src):
    if src.get('prism:volume'):
        volume = src['prism:volume']
    else:
        volume = '------'
    return volume


def get_start_page(src):
    if src.get('prism:startingPage'):
        starting_page = src['prism:startingPage']
    else:
        starting_page = '------'
    return starting_page


def get_end_page(src):
    if src.get('prism:endingPage'):
        ending_page = src['prism:endingPage']
    else:
        ending_page = '------'
    return ending_page


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


def get_isbn_from_dict(src):
    if src.get('dcterms:hasPart'):
        raw_isbn = src['dcterms:hasPart'][0]['@id']
        isbn_data = raw_isbn.replace('urn:isbn:', '')
        return isbn_data
    else:
        return ""


def formatting_article_object(result):
    t = "\t"
    result = f'""{t}""{t}{result["authors"]}{t}""{t}{result["title"]}{t}{result["journal_title"]}{t}{result["volume"]} \
        {t}{result["startPage"]}-{result["endPage"]}{t}{result["year_month"]}'
    return result


def formatting_book_object(result):
    t = "\t"
    result = f'""{t}""{t}{result["authors"]}{t}""{t}{result["title"]}{t}""{t}{result["publisher"]}{t}\
        {result["year_month"]}{t}""{t}""{t}""{t}""{t}""{t}{result["isbn"]}'
    return result


# def isbn_check():
#    past_data = open(sys.argv[2], mode='r', encoding='utf-8')
#    tsv_reader = csv.reader(past_data, delimiter='\t')
#    repetition_count = 0
#    isbn = get_isbn_from_dict(raw_isbn)
#    for row in tsv_reader:
#        past_isbn = row[13]
#        if isbn == past_isbn:
#            repetition_count += 1
#        else:
#            pass
#    past_data.close()
#    if repetition_count == 0:
#        return repetition_count
#    else:
#        pass
