
"""
#全体の目的
特定の出版社の新着書籍を自動的に取得
Excelなどで必要なもののみ選択できる状態にしたい
    →史学雑誌のフォーマットに取得したデータを落とし込む
    …完成したものをテンプレートにコピペ、細々と修正
​
#URLの作成
目的：
指定出版社から指定年に出版された図書を検索
​
サンプル：https://ci.nii.ac.jp/books/opensearch/search?publisher=東京大学出版会&year_from=2018&q=&format=json
​
指定要素
出版社：publisher=
出版年：year_from=
​
方針：
1. 対象の全出版社をリストかテキストファイルで作成しておく
    →対象が大きく変わらないなら、デフォルトでリストを固定してもいい
2. 出版年は年度ごとに必要に応じてスクリプトを変更
3. 出版社リストからfor文でURLリストを生成
​
#スクレイピング
import json, requests, re
​
CiNii BooksのJSON構造
Book ID:
    @graph [0] items
        -> それぞれの書籍のページは'rdfs:seeAlso' '@id'

タイトル：
    @graph [0] dc:title [0] '@id'
    副題は" : "で分けられているため、" : "でsplitすれば取れる。
    英題が入っている場合は=の有無で場合分け、そのあとに副題を分けます
    副題がない場合の場合分けは必要
    版: graph [0] "prism:edition"
​

著者：
    漢字: @graph [0] foaf:maker foaf:name [0] '@value'
    読み仮名: @graph [0] foaf:maker foaf:name [1] '@value' ←組み込む？
    著者が複数人の場合は", "で区切られる。最後の名前(唯一の場合はその名前)の最後には著・編がつく
    複数人いる場合は", "を中黒に置換
    翻訳書籍の場合の対応は別に検討が必要
        →翻訳の場合は著者と訳者は;で分かれている
​
その他要素：
    出版年月；
    @graph [0] dc:date
    年は20を消去、年月は"."で区切られるため、これを"-"に置換
​
    出版社；
        出版社リストのものを使う

    ISBN：
        @graoh [0] dcterms:hasPart [0] @id
        重複チェック用

不明な要素：
    分類(番号)、サイズ、ページ数、価格(、献本)

→これらは別個に調べる必要。ダブルチェックのためにここは残しておく
"""

import re
import json
import requests
import sys
import csv

# 先に事前準備
# 出版社リスト
publisher_list = ['岩波書店', '山川出版社', '藤原書店', '平凡社', '明石書店', '刀水書房', '中央公論新社',
                  'みすず書房', 'お茶の水書房', '原書房', '白水社', '河出書房新社', '彩流社', '勉誠出版',
                  '群像社', '恵雅堂', '水声社', '現代思潮新社', '成文社', '成文堂', '人文書院', '勁草書房',
                  '昭和堂', 'ミネルヴァ書房', '創文社', '教文館', '東洋書林', '柏書房', 'せりか書房',
                  '作品社', '丸善出版', '講談社学術文庫', 'ちくま新書',
                  '東京大学出版会', '京都大学学術出版会', '名古屋大学出版会', '東京外国語大学出版会', '北海道大学出版会',
                  '九州大学出版会',
                  '慶應義塾大学出版会', '早稲田大学出版部', '法政大学出版局', '関西学院出版会', '中央大学出版会',
                  '東洋大学出版会', '東海大学出版会']

# 結果を出力するファイルを指定
# result_file = open('※出力先のファイル.txt', mode='a', encoding='utf-8')
result_file = open("books_july20192.txt", mode='a', encoding='utf-8')


# メインの作業で使う関数を定義する
# それぞれに対しURLを作成、出版社とURLを対応させた辞書にする関数を作成
def make_publisher_dict(publisher_list):
    url_dict = {}
    for publisher in publisher_list:
        publisher_url = f"https://ci.nii.ac.jp/books/opensearch/search?publisher={publisher}&year_from=2019&q=&format=json"
        url_dict[publisher] = publisher_url

    return url_dict


# レスポンスからjsonのディクショナリーを生成する関数を作成
def fetch_json_convert_to_dict(url):
    res = requests.get(url)
    json_d = json.loads(res.text)
    return json_d


# 任意のJSONから生成されたディクショナリーから各書籍のJSON表記ページのURLを取得する関数を作成
def get_urls_from_json_dict(jd, publisher):
    urls = []
    books = jd['@graph'][0]
    if 'items' in books.keys():
        books = books['items']
        for book in books:
            book_url = book['rdfs:seeAlso']['@id'] if '@id' in book['rdfs:seeAlso'] else ""
            urls.append(book_url)
    else:
        result_file.write(f'{publisher}の書籍の取得に失敗しました')
    return urls


# タイトルを必要な形に整形する関数を作成。生データをタイトルと（あれば）サブタイトルに分割
# returnで複数の値を返しているので、厳密には文字列２つからなるタプルだけどアンパックします
def modify_title_data(title_data):
    # 不要な文字を消去する
    if "=" in title_data:
        title_data = re.sub(r'=.*$', '', title_data)
    else:
        pass
    # 取得した文字列をタイトルとサブタイトルに分割
    if ":" in title_data:
        title_data = title_data.split(' : ')
        title = title_data[0]
        subtitle = title_data[1]
    else:
        title = title_data
        subtitle = ''
    return title, subtitle


# 著者情報を整形する関数を作成。
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


# 日付情報を整形する関数を作成。
def modify_date_data(date_data):
    date_data = date_data.replace('20', '')
    if "." in date_data:
        dates = date_data.split(".")
        year = dates[0]
        month = dates[1]
        if len(month) == 1:
            month = ' ' + month
        else:
            pass
    else:
        year = date_data
        month = ""

    date = year + '-' + month
    return date


# ISBNを取得する関数を作成。
def get_isbn_from_dict(raw_isbn):
    if 'dcterms:hasPart' in raw_isbn.keys():
        raw_isbn = raw_isbn['dcterms:hasPart'][0]['@id'] if "@id" in raw_isbn['dcterms:hasPart'][0] else "isbn:取得失敗"
        if raw_isbn != "isbn:取得失敗":
            isbn_data = raw_isbn.replace('urn:isbn:', '')
        else:
            isbn_data = raw_isbn
        return isbn_data
    else:
        return ""


# 過去のデータとISBNを照合し、重複していなければ結果を渡す関数を作成。
def isbn_check():
    past_data = open("result_march.txt", mode='r', encoding='utf-8')
    tsv_reader = csv.reader(past_data, delimiter='\t')
    repetition_count = 0
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


# 関数の作成はここまで。以下からメインの作業


publisher_dict = make_publisher_dict(publisher_list)
for publisher, publisher_url in publisher_dict.items():
    jd = fetch_json_convert_to_dict(publisher_url)
    book_urls = get_urls_from_json_dict(jd, publisher)
    # 各書籍のJSONファイルをディクショナリーに変換
    for book_url in book_urls:
        try:
            book_dict = fetch_json_convert_to_dict(book_url)
            # book_dictは一冊分のJSONデータを元にした辞書型データ

            book_data = book_dict['@graph'][0]

            raw_title = book_data['dc:title'][0]['@value']
            title, subtitle = modify_title_data(raw_title)
            # これでタイトルの文字列を取得できた

            raw_author = book_data
            author = modify_author_data(raw_author)
            # 著者を取得

            raw_date = book_data['dc:date']
            date = modify_date_data(raw_date)
            # 発行年月を取得

            raw_isbn = book_data
            isbn = get_isbn_from_dict(raw_isbn)
            # ISBNを取得

            repetition = isbn_check()

            t = '\t'
            result = f'""{t}""{t}{author}{t}""{t}{title}{t}{subtitle}{t}{publisher}{t}{date}{t}""{t}""{t}""{t}""{t}""{t}{isbn}'
            if repetition == 0:
                result_file.write(result)
                result_file.write('\n')
            else:
                pass
            print(f'{publisher} finished')
        except ConnectionError:
            result_file.write(f'以下のURLについて通信に失敗しました。後ほど改めて試してください: {book_url}')
            result_file.write('\n')

result_file.close()

"""
if __name__ == "__main__":
    main()
"""
