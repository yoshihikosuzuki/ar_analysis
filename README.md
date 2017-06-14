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

`calc_car/1. Calculation and some plots on AR and CAR.ipynb`に一連の処理およびいくつかの図を書いている。

CARの検定は(ここ)[http://lipas.uwasa.fi/~bepa/EventStudies.pdf] に従った。

出力は`calc_car/car_exactT_sig`等。`sig`が付いているものは有意なCAR、`not_sig`が付いているものはそれ以外のCAR。

#### CAR結果(`https://github.com/yoshihikosuzuki/ar_analysis/blob/master/calc_car/car_exactT_sig`等)について

|article_id|PR_type|comp_code|CAR|t-statistics|
|:-:|:-:|:-:|:-:|:-:|
|PRのID|PRの種類|証券コード|CAR|t値|
|NIKPRLRSP050445_10072003|01: Product|7911|0.10449131277743914|2.325275468404645|

* 推定ウィンドウ=(-246, -30)、イベントウィンドウ=(-1, 1)、東証一部のみ、株価欠損値無し、片側5%で検定
  * => 有意に正なものは26845個中351個(1.3%) (`car_exactT_sig`)
* 片側10%で検定すると、708個(2.6%) (`car_exactT_alpha0.1_sig`)

## TF-IDFによるキーワード解析

有意なCARに特徴的な単語が存在するかどうか。

## TODO

* 東証一部以外の企業についても、とりあえずTOPIXを使ってCARを同様に計算する
