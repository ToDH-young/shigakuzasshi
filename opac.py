# coding: utf-8

import requests, bs4, csv, sys

url_list = []
journal = []
# url_file = open('./sample.txt')
url_file = open('./allbiblio2017u.txt')
url_reader = csv.reader(url_file, delimiter='\t')
for url in url_reader:
    url_list.append(url[1])
    journal.append(url[0])
    # opacのURLデータファイルを開き、URLのみ抽出したリストを作成する
result_file = sys.argv[1]
    # ターミナル上で指定したファイルを結果出力ファイルに指定

with open(result_file, mode = 'a', encoding = 'utf-8') as opac_result:
    for i in range(len(url_list)):
        try:
            res = requests.get(url_list[i])
                # URLリストのURLからHTMLファイルを取得。ここで失敗するとHTTPErrorかConnectionErrorが出る
            opac_soup = bs4.BeautifulSoup(res.text, 'lxml')
                # 取得してきたHTMLファイルをテキストとしてopac_soupに格納
            elem1 = opac_soup.select('h2.bb_ttl')
            for e1 in elem1:
                # selectで取って来た要素はリストとして返されるため、中身をstrに変換。elem2,3も同じ
                e1 = (e1.text) #.text: タグを削除
                opac_result.write(e1.strip() + '\n')
                    # opac_soupから必要な要素を抽出しresultファイルに書き込み
            elem2 = opac_soup.select('td.LOCATION > a')
                # td.LOCATIONタグ内にあるaタグのみを指定
            elem3 = opac_soup.select('td.VOLUMES')
                # td.VOLUMESタグを指定
            for i in range(len(elem2)):
                status = elem2[i].get_text() + ': ' + elem3[i].get_text().strip() + '\n'
                # ()のなかにごちゃごちゃ書くのが嫌だったので、搬入状況のstrを変数に格納
                opac_result.write(status)
            opac_result.write('\n')

        except TypeError:
            opac_result.write('直接OPACを確認してください')
        except ConnectionError:
            message = journal[i] + 'のURLを確認してください'
            opac_result.write(message)
