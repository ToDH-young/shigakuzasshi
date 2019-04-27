# -*- coding: utf-8 -*-

"""
データ加工の部分の処理を共通化
詳細についてはGoogle Spreadsheetを参照(CiNii articles/Books統合計画)
viewsでは、article部分でインスタンス生成→.search_article、book部分で同じくインスタンス生成→.search_booksとする
入力要求は期間と対象となるもの(雑誌/出版社、これらはリストで渡してもらうので共通で大丈夫)、resourceの種別(書籍か論文か)
formattingではjsonを渡して整形、それをマッピングし返す
"""

from .config import *
from .utils import *

class CiNii:
    def __init__(self, resource_type, target_list, since, until):
        self.api_url_for_article = ARTICLE_API
        self.api_url_for_books = BOOK_API
        self.result_format = "format=json"
        self.resource_type = resource_type
        self.target_list = target_list
        self.since = since
        self.until = until

    def search_article(self):
        article_list = []
        # url生成、ここではtarget_listにissnが格納されていると考える。
        for item in self.target_list:
            url = f"{self.api_url_for_article}issn={item}&year_from={self.since}&year_to={self.until}&{self.result_format}"
            article_dict = fetch_and_convert_json_to_dict(url)
            article_result = self.formatting(article_dict)
            article_list.append(article_result)
            sleep(1.5)
        return article_list

    def search_books(self):
        book_list = []
        for item in self.target_list:
            url = f"{self.api_url_for_books}publisher={item}&year_from={self.since}&year_to={self.until}&{self.result_format}"
            book_dict = fetch_and_convert_json_to_dict(url)
            book_result = self.formatting(book_dict)
            book_list.append(book_result)
            sleep(1.5)
        return book_list

    def formatting(self, json_dict):
        authors = modify_author_data(json_dict['authors'])
        title = modify_title_data(json_dict['article_title'])
        journal_title = modify_journal_title(json_dict['journal_title'])
        volume = json_dict['volume']
        startPage = json_dict['startPage']
        endPage = json_dict['endPage']
        year_month = modify_published_year_month(json_dict['year_month'])

        result = {
            'authors':authors,
            'title':title,
            'journal_title':journal_title,
            'volume':volume,
            'startPage':startPage,
            'endPage':endPage,
            'year_month':year_month
        }
        return result
