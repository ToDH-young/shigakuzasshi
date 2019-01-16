# coding: utf-8

"""
データ加工の部分の処理を共通化
詳細についてはGoogle Spreadsheetを参照(CiNii articles/Books統合計画)
"""

import json


class CiNii:
    def __init__(self):
        self.name = ""

    def get_title_from_dict(self, json_dict):
        title = json_dict['@graph'][0]['dc:title'][0]['@value']
        return title

    def modify_title_data(self, title):
        if '書評' in title:
            title_complete = title.replace('書評', '*')
        else:
            title_complete = title
        return title_complete

    def get_article_published_year_month(self, json_dict):
        date = json_dict['@graph'][0]['prism:publicationDate']
        return date


"""
    
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
                
                
        def formatting(self, 何か):
            if self.book:
                書籍の処理
            else:
                論文の処理
        # result = fill_format_with_article_data(FORMAT_STRING, article_dict)
                t = '\t'
                result = f'""{t}""{t}{authors}{t}""{t}{title}{t}{journal_title}{t}{volume}{t}{startPage}-{endPage}{t}{year_month}'
                result_file.write(result)
                result_file.write('\n')
"""