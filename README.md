# ar_analysis

プレスリリースのアブノーマルリターンに関する解析

### データ

`Reshape data.ipynb`で整形

* `pressrelease_all.csv`
 * 全てのプレスリリースのデータ(articleid, date, bodysubのタブ区切り)
* `listed_company`
 * 上場企業(企業名辞書で証券コードが存在する企業)のデータ(comp_name, address, sec_codeのタブ区切り)
* `kabuka_tse1`
 * 東証一部の株価データ(マーケットデータがTOPIXしかなかったので東証一部に限定した)
* `market_tse1`
 * TOPIXデータ
 
各種データ数等はipynbに記載
 
### プレスリリースと上場企業のマッチング
        
* [JUMAN++](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN++)を使う？
  1. プレスリリース本文・上場企業名ともに形態素に分解
  2. 企業名については、形態素ごとに完全マッチングを実行 -> 全て/ある一定以上マッチングしたらヒットとする
  3. 住所については、JUMAN++が地名の判定をしてくれるので、プレスリリース本文から連続した地名の部分を抽出 -> 正規化コンバータ、でマッチング？もしくは企業名と同様に形態素ごとにマッチング
