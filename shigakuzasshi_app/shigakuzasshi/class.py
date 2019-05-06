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

    def search(self):
        item_list = []
        # url生成、ここではtarget_listにissnが格納されていると考える。
        for item in self.target_list:
            if self.resource_type == 'articles':
                url = f"{self.api_url_for_article}issn={item}&year_from={self.since}&year_to={self.until}&{self.result_format}"
            else:
                url = f"{self.api_url_for_books}publisher={item}&year_from={self.since}&year_to={self.until}&{self.result_format}"

            src = fetch_and_convert_json_to_dict(url)  # TODO: formattingはまだarticle前提になっているので、書籍に対応できるように修正
            result = self.formatting(src)
            result['publisher'] = item
            item_list.append(result)
            sleep(1.5)
        return item_list

    def formatting(self, src):
        authors = get_authors_data(src)
        title = get_title_data(src)
        journal_title = get_journal_title_data(src)
        volume = get_article_volume(src)
        startPage = src['startPage'] if 'startPage' in src else ''
        endPage = src['endPage'] if 'endPage' in src else ''
        year_month = get_published_date_data(src)
        isbn = get_isbn_from_dict(src)

        result = {
            'authors': authors,
            'title': title,
            'journal_title': journal_title,
            'publisher': '',
            'volume': volume,
            'startPage': startPage,
            'endPage': endPage,
            'year_month': year_month,
            'isbn': isbn
        }
        return result
