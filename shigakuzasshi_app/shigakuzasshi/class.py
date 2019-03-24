# -*- coding: utf-8 -*-
# coding: utf-8

"""
データ加工の部分の処理を共通化
詳細についてはGoogle Spreadsheetを参照(CiNii articles/Books統合計画)
"""

import json
import requ
import requests


class CiNii:
    def __init__(self):
        self.name = ""

    def fetch_and_convert_json_to_dict(self, url):
        response = requests.get(url)
        json_dictionary = json.loads(response.text)
        return json_dictionary

    def get_title_from_dict(self, json_dict):
        title = json_dict['@graph'][0]['dc:title'][0]['@value']
        return title

    def modify_title_data(self, title):
        if '書評' in title:
            title_complete = title.replace('書評', '*')
        else:
            title_complete = title
        return title_complete

    def get_published_year_month(self, json_dict):
        date = json_dict['@graph'][0]['prism:publicationDate']
        return date

    def modify_published_year_month(self, date):
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

    def get_authors(self, json_dict):
        author = json_dict['@graph'][0]
        if 'dc:creator' in author.keys():
            authors = author['dc:creator'][0][0]['@value']
        else:
            authors = '------'
        return authors

    def modify_authors_data(self, authors):
        if '/' in authors:
            authors_complete = authors.replace('/', '・')
        else:
            authors_complete = authors
        return authors_complete

    def get_journal_title(self, json_dict):
        j_title = json_dict['@graph'][0]['prism:publicationName'][0]['@value']
        return j_title

    def modify_journal_title(self, j_title):
        if '=' in j_title:
            split_j_title = j_title.split('=')
            j_title_complete = split_j_title[0]
        else:
            j_title_complete = j_title
        return j_title_complete

    def get_article_volume(self, json_dict):
        raw_volume = json_dict['@graph'][0]
        if 'prism:number' in raw_volume.keys():
            volume = raw_volume['prism:number']
        else:
            volume = '------'
        return volume

    def get_start_page(self, json_dict):
        raw_startingpage = json_dict['@graph'][0]
        if 'prism:startingPage' in raw_startingpage.keys():
            startingpage = raw_startingpage['prism:startingPage']
        else:
            startingpage = '------'
        return startingpage

    def get_end_page(self, json_dict):
        raw_endingpage = json_dict['@graph'][0]
        if 'prism:endingPage' in raw_endingpage.keys():
            endingpage = raw_endingpage['prism:endingPage']
        else:
            endingpage = '------'
        return endingpage
