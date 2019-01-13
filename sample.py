# classを使ってJSONファイルを処理してみる
# 本ファイルはCiNii.pyで作成したクラス操作のテスト用

from CiNii import CiNii
import json
import requests


res = requests.get('https://ci.nii.ac.jp/naid/40021719192.json')
json_d = json.loads(res.text)

data = CiNii()
title = data.get_article_title_from_dict(json_d)
print(title)
