import time
import requests
import json
import pandas as pd
import numpy as np
import unicodedata
import MeCab
from collections import Counter
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ipadic
import re

# user_idはtwicasサイトのurlから取得できます(https://twitcasting.tv/gazyumarma22の例)
# アクセストークンを入れてください
user_name = "gazyumarma22" 
bearer_token = ""  

def get_last_movie_id(user_name, bearer_token):
    url = f"https://apiv2.twitcasting.tv/users/{user_name}"
    headers = {
    "Accept": "application/json",
    "X-Api-Version": "2.0",
    "Authorization": f"Bearer {bearer_token}"  
}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        last_movie_id = data["user"]["last_movie_id"]
        return last_movie_id
    else:
        return f"Failed to get data: {response.status_code}"


movie_id = get_last_movie_id(user_name, bearer_token)
print(f"Last Movie ID: {movie_id}")

# 設定
base_url = f"https://apiv2.twitcasting.tv/movies/{movie_id}/comments"
headers = {
    "Accept": "application/json",
    "X-Api-Version": "2.0",
    "Authorization": f"Bearer {bearer_token}" 
}

all_comments = []
offset = 0
limit = 40
counts=0

while True:
    params = {
        "offset": offset,
        "limit": limit
    }
    
    response = requests.get(base_url, headers=headers,params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break

    
    data = response.json()
    comments = data.get("comments", [])

    if not comments:
        break
    
    for comment in comments:
        all_comments.append(comment["message"])
        # print(all_comments)
    
    offset += limit
    counts += limit
    print("success to get comments")
    

# コメントを一つの文字列に結合
text = "".join(all_comments)

print(f"comments counts: {counts}")
# sample.txtファイルに書き込み
with open("sample.txt", "w", encoding="utf-8") as file:
    file.write(text)

# sample.txtからテキストを読み込み
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return str(e)

file_path = 'sample.txt'
text = read_file(file_path)
# print(text)

# 関数の設定
def mecab_tokenizer(text):
    mecab = MeCab.Tagger(ipadic.MECAB_ARGS)  # MeCab.Tagger オブジェクトの初期化

    replaced_text = unicodedata.normalize("NFKC", text)
    replaced_text = replaced_text.upper()
    replaced_text = re.sub(r'[【】 () （） 『』　「」]', '', replaced_text)  # 【】 () 「」　『』の除去
    replaced_text = re.sub(r'[\[\［］\]]', ' ', replaced_text)  # ［］の除去
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)  # メンションの除去
    replaced_text = re.sub(r'\d+\.*\d*', '', replaced_text)  # 数字の除去

    parsed_lines = mecab.parse(replaced_text).split("\n")[:-2]

    # 表層系を取得
    surfaces = [l.split("\t")[0] for l in parsed_lines]
    # 品詞を取得
    pos = [l.split("\t")[1].split(",")[0] for l in parsed_lines]
    # 名詞、動詞、形容詞に絞り込み
    target_pos = ["名詞", "動詞", "形容詞"]
    token_list = [t for t, p in zip(surfaces, pos) if p in target_pos]

    # ひらがなのみの単語を除く
    kana_re = re.compile("^[ぁ-ゖ]+$")
    token_list = [t for t in token_list if not kana_re.match(t)]

    # 各トークンを少しスペースを空けて（' '）結合
    return ' '.join(token_list)

# 関数の実行
words = mecab_tokenizer(text)

# フォントの設定(OSによってフォントの場所が違うので気を付ける)
font_path = '/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc'
# 色の設定
colormap = "Paired"

wordcloud = WordCloud(
    background_color="white",
    width=800,
    height=800,
    font_path=font_path,
    colormap=colormap,
    stopwords=["する", "ある", "こと", "ない"],
    max_words=100,
).generate(words)

plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
# savefig の前にshowすると保存できないので逆にしない
plt.savefig(f"results/{user_name}.png") 
plt.show()



