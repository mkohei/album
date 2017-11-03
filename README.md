# album

画像群と設定ファイルからアルバムページを自動生成するスクリプト

## TODO(構成)

### WEBページ

* [x] コンスタントだけを別ファイルに作りたい(templateが変わっても使えるため? -> 関数化しろ！)
* [ ] JS, CSS等のファイル作成は，コピー
* [ ] サイドメニューから他年度，krlabHP, KUTHP
* [ ] SNS (youtube)
* [ ] 日付へのナビ - 日付だと多いので月ごとは？
* [ ] 動画対応 -> 動画を貼る? or サムネ and youtubeへのリンク

### 画像

* [x] EXIFデータから自動日付割当
* [ ] 画像コメント(title?), 画像コメント, title等を直接書くようにしたくない
* [x] EXIFデータのmodel(?)から全天球画像判定(?)
* [ ] goodボタンやコメント機能, download数
* [x] download
* [x] 360viewer

### 内部仕様

* [ ] downloadや360viewerページ名用にIDをつける(date + orderとか, img名はそのまま？)
* [ ] HTMLコード作成の関数化

### 設定方法

* [ ] web上でupdate
