# Text_Mining_App
文書データセットから学習データを作成するアプリを作成。<br><br>
何も整形されていないデータセットに分かち書きや単語整形を施して学習データに変換できるようになった。<br><br>
<h3>Web日記版</h3>
<ul>
  <li>
    <a href="https://web-diarys.web.app/App/public6/index.html">Docker+Djangoでテキストマイニングアプリを作成</a>
  </li>
</ul>
<br>

<h3>開発背景</h3>
機械学習では、前処理として以下の処理をする必要がある。<br><br>
<ul>
  <li>特定のデータ行のみ摘出する</li><br>
  <li>特定のデータ列のみ摘出する</li><br>
  <li>数字や記号など、意味関数が低い単語を0などの単語に統一する</li><br>
</ul>
上記の要件を満たす前処理プログラムを目的に応じて作成し直すのが面倒だったため、予め必要な機能をアプリにして実装することにした。<br><br>


<h3>アーキテクチャ</h3>
Django の MTV(Model, Template, View)  モデルを元に設計。<br><br>
<ul>
    <li>M : データベースと連携を取る</li><br>
    <li>T : HTMLファイルとして画面に反映させる</li><br>
    <li>V : Modelから取得したデータの見せ方を定義する</li>
</ul>
<img width="917" alt="image" src="https://user-images.githubusercontent.com/116938721/236974967-15c98eed-7249-4c62-adc8-3f3b36056f20.png">
<br><br>
 
<h3>メイン画面</h3>
用途に応じた選択肢を選び、「ファイルを作成する」ボタンを押すことでファイルがダウンロードされます。<br><br>
ファイル拡張子は txt, csv, tsv から選択することができます。<br><br>
<div class="work-image">
 　<img width="550" alt="image" src="https://user-images.githubusercontent.com/116938721/236784671-93b95cdf-7e3c-4327-b02e-9075d4257740.png">
</div>
<br><br>
 
<h3>データセット登録画面</h3>
データベースにデータを登録する機能。<br><br>
開発環境ではsqlite3, 本番環境ではpostgresqlを使用している。<br><br>
<div class="work-image">
 　<img width="569" alt="image" src="https://user-images.githubusercontent.com/116938721/236785014-a8ddecaa-7039-48b7-ad0a-1276342c707a.png">
</div>
<br><br>
 
<h3>データセット削除画面</h3>
登録されているデータセットを削除する機能。<br><br>
<div class="work-image">
 　<img width="490" alt="image" src="https://user-images.githubusercontent.com/116938721/236785431-f8d69f4b-498d-4403-984a-5dfd7dd6f3db.png">
</div>
<br><br>

<h3>ログイン画面</h3>
最初はこの画面になっているのでログインしないと使用できない状態になっている。<br><br>
データセットの二次配布が禁止されているため実装した。<br><br>
<div class="work-image">
  <img width="700" alt="image" src="https://user-images.githubusercontent.com/116938721/236797569-08f71249-52ca-4ede-a872-76cb92a17371.png">
</div>
<br><br>

<h3>データベースについて</h3>
Django administration というデータベース管理機能を使用している。<br><br>
データベースはsqlite3(開発環境)とpostgresql(本番環境)を使用。<br><br>

<h3>データの保存形式</h3>
<div class="work-image">
   <img width="718" alt="image" src="https://user-images.githubusercontent.com/116938721/236798849-212dede9-8dee-422a-ac98-0c5642fc5ea8.png">
</div>
<br><br>

<h3>データリスト</h3>
<div class="work-image">
   <img width="722" alt="image" src="https://user-images.githubusercontent.com/116938721/236799023-96fca806-394b-4788-b8e5-2f928da2ecd5.png">
</div>
<br><br>

<h2>各選択肢の仕様</h2>

<h3><font color="red">整形形式</font></h3>
「分かち書きのみ」の場合は何も整形しない。<br><br>
「分かち書き+整形」の場合は以下の処理をして出力する。<br>
<ul>
   <li>数字を0に置き換える</li><br>
   <li>記号を削除する</li><br>
   <li>カンマを削除する</li><br>
   <li>タブを削除する</li><br>
   <li>英単語は全て小文字にする</li><br>
</ul>

<h3><font color="red">出力形式</font></h3>
以下のフォーマットから選択して出力する。<br>
<ul>
   <li>txt (Text Documents)</li><br>
   <li>csv (Comma Separated Values )</li><br>
   <li>tsv (Tab Separated Values )</li><br>
</ul>

<h3><font color="red">ファイル名を出力</font></h3>
「Yes」の場合はファイル名を出力する。<br><br>
 逆にファイル名は出力したくない場合もあったりするので、その場合は「No」を選択しておく。<br><br>

<h3><font color="red">正解ラベルを出力(欠損値なし)</font></h3>
「Yes」の場合は正解ラベルを出力する。<br><br>
「欠損値なし」にしているため全ての正解ラベルが出力される。<br><br>

<h3><font color="red">正解ラベルを出力(欠損値あり)</font></h3>
「10%」~「90%」を選択した場合は正解ラベルを出力する。<br><br>
「欠損値あり」にしているため一部の正解ラベルが出力されない。<br><br>
例えば、選択肢で10%を選択した場合は全データの10%がラベルなしデータとして出力される。<br><br>
一部の正解ラベルを隠して学習する半教師あり学習で使用する。<br><br>

<h3><font color="red">文章を出力</font></h3>
「Yes」の場合は文章を出力する。<br><br>
文章を出力したくない場合はあまりないと思ったが一応選択肢にしている。<br><br>

<h3><font color="red">指定されたデータのみ出力</font></h3>
特定のデータだけ出力する場合はファイル名をtxtファイルに記述してアップロードする。<br><br>
以下のように、1行毎に区切ってファイル名を入力する。<br><br>
dokujo-tsushin-4782522.txt<br>
dokujo-tsushin-4788373.txt<br>
dokujo-tsushin-4791665.txt<br><br>
データベースに存在しないファイル名はスルーしている。<br><br>
txt, csv 以外のファイルをアップロードした場合はエラーメッセージを表示する。
