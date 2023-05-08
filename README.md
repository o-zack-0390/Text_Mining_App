# Text_Mining_App
文書データセットから学習データを作成するアプリを作成しました。<br><br>
何も整形されていないデータセットに分かち書きや単語整形を施して学習データに変換します。<br><br>
Web日記版:<a href="https://web-diarys.web.app/App/public6/index.html">Text_Mining_App</a>
<br><br>
 
<h3>メイン画面</h3>
用途に応じた選択肢を選び、「ファイルを作成する」ボタンを押すことでファイルがダウンロードされます。<br><br>
ファイル拡張子は txt, csv, tsv から選択することができます。<br><br>
<div class="work-image">
 　<img width="550" alt="image" src="https://user-images.githubusercontent.com/116938721/236784671-93b95cdf-7e3c-4327-b02e-9075d4257740.png">
</div>
<br><br>
 
<h3>データセット登録画面</h3>
データベースにデータを登録する機能です。<br><br>
開発環境ではsqlite3, 本番環境ではpostgresqlを使用しています。<br><br>
<div class="work-image">
 　<img width="569" alt="image" src="https://user-images.githubusercontent.com/116938721/236785014-a8ddecaa-7039-48b7-ad0a-1276342c707a.png">
</div>
<br><br>
 
<h3>データセット削除画面</h3>
登録されているデータセットを削除する機能です。<br><br>
<div class="work-image">
 　<img width="490" alt="image" src="https://user-images.githubusercontent.com/116938721/236785431-f8d69f4b-498d-4403-984a-5dfd7dd6f3db.png">
</div>
<br><br>

<h3>ログイン画面</h3>
最初はこの画面になっているためログインしないと使用できません。<br><br>
データセットの二次配布が禁止されているので実装しました。<br><br>
<div class="work-image">
  ![image](https://user-images.githubusercontent.com/116938721/236785637-ba378d78-3566-4513-8a9a-edf181aa8b9d.png)
</div>
