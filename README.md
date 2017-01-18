# ar_analysis

プレスリリースのアブノーマルリターンに関する解析

### データ

`Reshape data.ipynb`で整形した。各種データ数等はipynbに記載してある。
今回の株価データには株価指数がTOPIXしかなかったので、解析対象は東証一部上場企業に限定した(`listed_company`自体には全ての上場企業が含まれている)。

* `pressrelease_all.csv`
 * 全てのプレスリリースのデータ(articleid, date, bodysubのタブ区切り)
* `listed_company`
 * 上場企業(企業名辞書で証券コードが存在する企業)のデータ(comp_name, address, sec_codeのタブ区切り)
* `kabuka_tse1`
 * 東証一部の株価データ(マーケットデータがTOPIXしかなかったので東証一部に限定した)
* `market_tse1`
 * TOPIXデータ

```txt:昔の情報
### プレスリリースと上場企業のマッチング(`Matching.ipynb`)

現状では、上場企業のデータをもとにプレスリリースに完全一致検索をかける方針で行っている。出力は`matchings`。

1. 企業名は企業名辞書のものをそのまま使用し、完全一致でヒットとする
2. 住所は企業名辞書のものを正規化した後、市区町村名だけを(最大2つ)抽出し、どれか1つでも完全一致したらヒットとする
 * 住所を記載する場合、都道府県名は無くても理解できる場合がああるが、市区町村名を全て書かないと意味がほとんどないという仮定に基づく
 * また、都道府県名だと関係のないヒットがありそうだが、市区町村名だとその可能性が低そうだという理由もある
3. 企業名・住所ともにヒットしたら結果に追加する
 
#### 改善した方が良さそうな点

* 企業名の揺らぎ
 * 英語表記とカタカナ表記
 * `・`等
 * `株式会社`、`ホールディングス`等 -> 取り除いてから検索？池内さんの`func_nayose.R`が使えるはず
* 住所の揺らぎ
 * プレスリリース本文から住所を表す部分だけを抽出できれば、お互いの正規化の結果同士で比較するのが最善か
* `headline`にしか企業名が含まれないものや、企業名だけで住所を含まないものが散見される
* 短くて複雑度の低い企業名で、かつ住所が都内だったりするとfalse-positive hitが起こりやすい
 * "高島", "ランド", "アーク"といった比較的よくある企業名で見られた
 * 都内は区名の次まで検索したいが、区名までしか記載していないことも多い。。
 * 企業名と住所が近くにあることの判定？思い切って複雑度の低い名前を持つ企業を取り除く？
```

### 新しいマッチング(`New matching.ipynb`)

池内さんから頂いた`prdata_subj_db.csv`に各プレスリリースの企業名情報(`subj`)があったので、それを使用することにした。

* 住所は用いず、`subj`をそのままマッチング結果とした
* アブノーマルリターンを計算する際に、`subj`が上場企業名リストに存在していなかったら排除している

### アブノーマルリターンの計算(`Calculate abnormal return.ipynb`、新: `New calculate CAR.ipynb`)

* (プレスリリースが出た)日付を指定すると、その日を0として、(-246, -30)[日]の区間と(-1, 1)の区間でのその企業とTOPIXの株価データからアブノーマルリターンを計算
 * 企業の株価データには(非取引日以外でも)欠損値を含むものがあるが、日数は欠損値を除いて計上した(日付はTOPIXと合わせてある)
* アブノーマルリターン計算には[PythonFinance](https://github.com/danielfrg/PythonFinance)の`events/EventStudy.py`を参考にした
 1. (欠損値を除いた)前日との株価の比(return)を計算
 2. (-246, -30)のreturnデータでTOPIX - 企業間の線形回帰モデル作成
 3. モデルを(-1, 1)に適用し、指定された日付前後のexpected returnを計算
 4. 実際のreturnとの差を取り(abnormal return)、その(-1, 1)での和(cumulative abnormal return)を返す
* 手法として古い可能性がある？
* **同一日、同一企業に複数のプレスリリースがある場合に考慮できていない**

計算結果は`car.new`に記載(プレスリリースID、タイプ、証券コード、cumulative abnormal returnのタブ区切り)。

### アブノーマルリターンの値に関する簡単な分析(`Plot car results.ipynb`、新: `New analyze CAR .ipynb`)

* 全部で47301 (旧: 41950)データ
* 頻度分布 -> 正規分布との相違
 * 中心はほぼ0%で、尖った形状
* 最大値、最小値はそれぞれ920% (旧: 70%), -110%
* 10%以上の影響を与えたもののうち、正の影響は590 (旧: 670)個、負の影響は337 (旧: 426)個
 * これらは全データのうち約2%
* 平均値の降順に各タイプを並べたものは以下の表の通り

<img src=https://qiita-image-store.s3.amazonaws.com/0/81825/0fd33507-3987-98f0-a567-e3c2569bd1b2.jpeg width=1000px>

### tf-idf (`Calculate tf-idf.ipynb`)

CARが高いようなPRについて、各単語のtf-idfを計算した。

(ipynbの数式がgithubだと一部表示されなくなっているので後で修正、もしくは生データのlatexを参照)

```
全PR数 高CAR群のPR数
単語 tf-idf 全PRのうちその単語が出現した数 高CAR群のPRのうちその単語が出現した数
…
```
↑各値の説明

#### "01: Product", CAR = 0% もしくは 1.48% (75% quantile) で分割

|0%|1.48%|
|:-:|:-:|
|<img src=https://qiita-image-store.s3.amazonaws.com/0/81825/1cbbdef3-23de-9be0-9979-a7abf4ace775.jpeg>|<img src=https://qiita-image-store.s3.amazonaws.com/0/81825/2cbce839-40e2-dd8a-9bda-888ed93efc29.jpeg>|

```
#### 全タイプのデータ(`tfidf.all`)

<img src=https://qiita-image-store.s3.amazonaws.com/0/81825/38c8cf98-df4b-d2ac-039c-54ac369a3cf3.jpeg width=300px>

#### "01: Product"に限定したデータ(`tfidf.product`)

<img src=https://qiita-image-store.s3.amazonaws.com/0/81825/fdc5eee9-afdb-585f-341e-2558e526f638.jpeg width=300px>

因果関係は無視したとしても、

* URLを入れると株価が上がる？
* "東京"・"本社"があると株価が上がる？
* 2008年・2009年だと株価が上がった？？
* "代表"・"取締役"を書くと株価が上がる？？？
```

### doc2vecを使った分析

articleid: CARの情報がある時に、articleid -> bodysub -> doc2vec(bodysub): CARとして、プレスリリース本文とCARの値の関係性を述べたい。

* `Doc2Vec.ipynb`
 * 全てのプレスリリース本文をMeCabで形態素に分割し、doc2vecの学習を行う
 * CARが存在するプレスリリースのベクトル表現を出力
* `*.ipynb`
 * 入力: プレスリリースのベクトル表現、教師データ: CARで学習器を作成
