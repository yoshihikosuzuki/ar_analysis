# ar_analysis

プレスリリースのアブノーマルリターンに関する解析

(前回(2016年度)の古い解析内容はREADMEも含めて全て`old/`ディレクトリ以下に移動した。)

## データ

|種類|ファイル名(自分用)|データ数|その他|
|:-:|:-:|:-:|:-:|
|日経プレスリリース|pressrelease_all_normalized.csv|336297 (PR)|articleid, date, bodysubのタブ区切り<br>2003~2014年|
|日経プレスリリース分類|pressrelease_info.csv|354691 (PR)|池内さんに頂いたもの|
|上場企業|listed_company|3564 (社)|comp_name, address, sec_codeのタブ区切り|
|東証一部の株価|kabuka_tse1|1788 (社)|マーケットデータがTOPIXしかなかったため<br>欠損値あり|
|TOPIX|market_tse1|||

## プレスリリース-企業マッチング

`address-matching`レポジトリを参照(その中の`src/all.out.matching`がマッチング結果。列名などは以下を参照)。

結果の数は以前の336,271 -> 72,040と大幅に減ったが、見た感じ精度良く(precision高く)マッチングできていそう。

#### マッチング結果(`https://github.com/yoshihikosuzuki/ar_analysis/blob/master/calc_car/all.out.matching`)について

|'article_id'|'date'|'sentence'|'comp_code'|'comp_name'|'address_pr'|'add_ress_lc'|'score'|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|プレスリリースのID|PRの日付|PRの住所の直前40文字|上場企業の証券コード|企業名|PRから抽出した住所|上場企業の住所|スコア(上のレポジトリ参照)|
|NIKPRLRSP038060_07012003|20030107|着信メロディ配信サービスヤマハ『美麗鈴(メロリン)』を開始ヤマハ株式会社(本社:|7951|ヤマハ|静岡県 None 浜松市 中区 中沢町 None None 10 1 None None|静岡県 None 浜松市 中区 中沢町 None None 10 1 None None|9|

## Cumulative Abnormal Return (CAR)計算

解析内容は以前と同じ(`calc_car/Calculate CAR.ipynb`を参照)で、`calc_car/car.all`に出力。

27,840個の結果が得られた(前回は47,301個)。

#### CAR結果(`https://github.com/yoshihikosuzuki/ar_analysis/blob/master/calc_car/car.all`)について

|article_id|PR_type|comp_code|CAR|R-value|p-value|
|:-:|:-:|:-:|:-:|:-:|:-:|
|PRのID|PRの種類|証券コード|CAR|相関係数|p値|
|NIKPRLRSP117970_09122005|05: PR|1812|-0.0322159540276|0.710436457798|1.19732463497e-34|

*NOTE:現在は相関係数とp値はexpectedの計算に用いたものになっている(つまり、(-246, -30)[日]の区間; 本当は(-1, 1)の区間の有意差を見たい

## CAR結果について

[ここ](http://dss.princeton.edu/online_help/stats_packages/stata/eventstudy.html#car)にしたがってCARの検定を行う。

CAR = sum of AR なので、検定のためのaveraged AR (AAR) = CAR / window size (= 3)でよい(検定力がダメそう)。

そもそも、このt検定だと「PR発表日前後での株価上昇」を見ていないことになる。。むしろ回帰の方がよい？

## TODO

* 東証一部以外の企業についても、とりあえずTOPIXを使ってCARを同様に計算する
* 有意なCARを持つPR群からキーワード特定