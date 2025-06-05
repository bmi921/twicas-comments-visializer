# twicas-comments-visializer

`user_name`は
twicas サイトの url から取得できます
https://twitcasting.tv/gazyumarma22の例なら、
`user_name = "gazyumarma22"`としてください
また、twicas からアクセストークンを取得し入れてください
`bearer_token = ""`

```bash
git clone https://github.com/bmi921/twicas-comments-visializer
cd ./twicas-comments-visializer
pip install　-r requirements.txt
python main.py
```

ツイキャスの大手配信者のコメント欄をワードクラウドで可視化する。  
クローンした後に、main.py に含まれるパッケージをインストールしてください。
requirement.txt にパッケージ群は書いてあります。
janome, wordcloud その他周辺技術ライブラリをインストールすれば正常に動きます。

# 解析例
![Image](https://github.com/user-attachments/assets/b1d51429-5f1d-447a-8092-c3d2012629b3)
