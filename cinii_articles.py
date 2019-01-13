#!/usr/bin/env python3
# coding: utf-8


# 目的：CiNii articlesのURLを作成
# 完成版

import requests, re, sys
import gspread
import json
import oauth2client.client
from typing import Any
from time import sleep

# APIを用いて、google spreadsheetからISSNのリストを作成
json_key = json.load(open('Project-4f8513313c78.json'))
scope = ['http://spreadsheets.google.com/feeds']
credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'],
                                                                json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)

wb = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/10JhDeGJgsAf_2jDjdTpKJy60Zc6EanrJsPj8141FH4c/edit#gid=1968944433")
ws = wb.worksheet("リポジトリ")

issn_list = ws.col_values(2)
keys_list = ws.col_values(1)
# key_value_dict = dict(zip(keys_list, values_list))

# print(issn_list)
# issn_list = ['0385-4841', '0288-1802', '0389-3138', '0447-9114', '0491-3329', '1346-7182', '0563-8186', '1884-1732', '0386-8729', '1348-2793']


# ISSNのリストをもとに、URLを自動生成する。
url_list = []
for issn in issn_list:
    url = f"http://ci.nii.ac.jp/opensearch/search?issn={issn}&year_from=2018&format=json"
    url_list.append(url)

# print(url_list)

result_file = open('cinii_articles.txt', mode='a', encoding='utf-8')


# 以下で、jsonの辞書からそれぞれのデータを取得する関数を作成

def get_article_title_from_dict(json_dict):
    title = json_dict['@graph'][0]['dc:title'][0]['@value']
    return title


def modify_title_data(title):
    if '書評' in title:
        title_complete = title.replace('書評', '*')
    else:
        title_complete = title
    return title_complete


def get_atricle_published_year_month(json_dict):
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


def get_article_authors(json_dict):
    author = json_dict['@graph'][0]
    if 'dc:creator' in author.keys():
        authors = author['dc:creator'][0][0]['@value']
    else:
        authors = '------'
    return authors


def modify_authors_data(authors):
    if '/' in authors:
        authors_complete = authors.replace('/', '・')
    else:
        authors_complete = authors
    return authors_complete


def get_journal_title(json_dict):
    j_title = json_dict['@graph'][0]['prism:publicationName'][0]['@value']
    return j_title


def modify_journal_title(j_title):
    if '=' in j_title:
        splited_j_title = j_title.split('=')
        j_title_complete = splited_j_title[0]
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


def fetch_and_convert_article_json_to_dict(url):
    article_dict = {}
    json_dict = fetch_and_convert_json_to_dict(url)

    article_dict['authors'] = get_article_authors(json_dict)
    article_dict['article_title'] = get_article_title_from_dict(json_dict)
    article_dict['journal_title'] = get_journal_title(json_dict)
    article_dict['volume'] = get_article_volume(json_dict)
    article_dict['startPage'] = get_start_page(json_dict)
    article_dict['endPage'] = get_end_page(json_dict)
    article_dict['year_month'] = get_atricle_published_year_month(json_dict)

    return article_dict


for i in range(len(url_list)):
    sleep(2)
    jd = fetch_and_convert_json_to_dict(url_list[i])
    article_urls = get_urls_from_json_dict(jd)
    # print(article_urls)

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

result_file.close()