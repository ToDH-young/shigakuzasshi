
# 目的：CiNii articlesのURLを作成
# 完成版

import requests
import re
import sys
import gspread
import json
import oauth2client.client
from typing import Any
from time import sleep

# APIを用いて、google spreadsheetからISSNのリストを作成　※apiproject~~のjsonファイルを用意する
json_key = json.load(open('apiproject-9ead6aae00b0.json'))
scope = ['http://spreadsheets.google.com/feeds']
credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'],
                                                               json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)

wb = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/10JhDeGJgsAf_2jDjdTpKJy60Zc6EanrJsPj8141FH4c/edit#gid=1968944433")
ws = wb.worksheet("総図地下+史編+法図+文図+西洋史+東文研")

issn_list = ws.col_values(2)
keys_list = ws.col_values(1)
# key_value_dict = dict(zip(keys_list, values_list))


# issn_list = ['0385-4841', '0288-1802', '0389-3138', '0447-9114', '0491-3329', '1346-7182', '0563-8186', '1884-1732', '0386-8729', '1348-2793']


# ISSNのリストをもとに、URLを自動生成する。
url_list = []
for issn in issn_list:
    issn = issn.strip()
    url = f"http://ci.nii.ac.jp/opensearch/search?issn={issn}&year_from=2019&format=json"
    url_list.append(url)


result_file = open('総図地下+史編+法図+文図+西洋史+東文研.txt', mode='a', encoding='utf-8')


# 以下で、jsonの辞書からそれぞれのデータを取得する関数を作成

def get_article_title_from_dict(json_dict):
    title = json_dict['dc:title'][0]['@value']
    return title


def get_article_published_year_month(json_dict):
    date = json_dict['prism:publicationDate'] if 'prism:publicationDate' in json_dict else '取得失敗'
    return date


def get_article_authors(json_dict):
    if 'dc:creator' in json_dict.keys():
        authors = json_dict['dc:creator'][0][0]['@value']
    else:
        authors = '取得失敗'
    return authors


def get_journal_title(json_dict):
    if 'prism:publicationName' in json_dict:
        j_title = json_dict['prism:publicationName'][0]['@value']
    elif 'dc:title' in json_dict:
        j_title = json_dict['dc:title'][0]['@value']
    else:
        j_title = "タイトル取得失敗"
    return j_title


def get_article_volume(json_dict):
    if 'prism:number' in json_dict.keys():
        volume = json_dict['prism:number']
    else:
        volume = '取得失敗'
    return volume


def get_start_page(json_dict):
    if 'prism:startingPage' in json_dict.keys():
        startingpage = json_dict['prism:startingPage']
    else:
        startingpage = '取得失敗'
    return startingpage


def get_end_page(json_dict):
    if 'prism:endingPage' in json_dict.keys():
        endingpage = json_dict['prism:endingPage']
    else:
        endingpage = '取得失敗'
    return endingpage


def get_urls_from_json_dict(json_dict):
    urls = []
    if 'items' in json_dict.keys():
        dictionary_in_list = json_dict['items']
        # dictionary_in_listはリスト型
        for dictionary in dictionary_in_list:
            article_url = dictionary['rdfs:seeAlso']['@id']
            urls.append(article_url)
    else:
        site_id = json_dict['@id']
        target_pattern = r'(?<=issn=).*(?=&year)'
        failed_issn = target_pattern.match(target_pattern, site_id).group()
        message = f'以下の雑誌の記事の取得に失敗しました: issn={failed_issn}'
        result_file.write(message)
    return urls


def modify_title_data(title):
    if '書評' in title:
        title_complete = title.replace('書評', '*')
    else:
        title_complete = title
    return title_complete


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


def modify_authors_data(authors):
    if '/' in authors:
        authors_complete = authors.replace('/', '・')
    else:
        authors_complete = authors
    return authors_complete


def modify_journal_title(j_title):
    if '=' in j_title:
        splited_j_title = j_title.split('=')
        j_title_complete = splited_j_title[0]
    else:
        j_title_complete = j_title
    return j_title_complete



def fetch_and_convert_json_to_dict(url):
    response = requests.get(url)
    json_dictionary = json.loads(response.text)
    return json_dictionary


def fetch_and_convert_article_json_to_dict(url):
    article_dict = {}
    json_dict = fetch_and_convert_json_to_dict(url)
    target_dict = json_dict['@graph'][0]

    article_dict['authors'] = get_article_authors(target_dict)
    article_dict['article_title'] = get_article_title_from_dict(target_dict)
    article_dict['journal_title'] = get_journal_title(target_dict)
    article_dict['volume'] = get_article_volume(target_dict)
    article_dict['startPage'] = get_start_page(target_dict)
    article_dict['endPage'] = get_end_page(target_dict)
    article_dict['year_month'] = get_article_published_year_month(target_dict)

    return article_dict

journal_number = 1
for i in range(len(url_list)):
    sleep(2)
    jd = fetch_and_convert_json_to_dict(url_list[i])
    print(jd)
    article_urls = get_urls_from_json_dict(jd['@graph'][0])

    for article_url in article_urls:
        article_dict = fetch_and_convert_article_json_to_dict(article_url)
        # json_dict = fetch_and_convert_json_to_dict(article_dict)

        authors = modify_authors_data(article_dict['authors'])
        title = modify_title_data(article_dict['article_title'])
        journal_title = modify_journal_title(article_dict['journal_title'])
        volume = article_dict['volume']
        startPage = article_dict['startPage']
        endPage = article_dict['endPage']
        year_month = modify_published_year_month(article_dict['year_month'])

        # result = fill_format_with_article_data(FORMAT_STRING, article_dict)
        t = '\t'
        result = f'""{t}""{t}{authors}{t}""{t}{title}{t}{journal_title}{t}{volume}{t}{startPage}-{endPage}{t}{year_month}'
        result_file.write(result)
        result_file.write('\n')
    print(f'{journal_number} journal completed')
    journal_number += 1


result_file.close()















