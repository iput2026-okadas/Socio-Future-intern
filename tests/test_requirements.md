# MySQL Backup Tool - Test Requirements

このドキュメントでは、インターンシップで開発するバックアップツールについて、確認してほしい動作をまとめています。

完成コードそのものではなく、**「どのような状態になれば正しく実装できたと判断できるか」**を示しています。

すべての項目を一度に実装する必要はありません。
進捗に応じて、★ → ★★ → ★★★ の順に確認してください。

---

# 1. テスト環境

サンプルデータベースとして、次のSQLを使用します。

```text
sql/setup_sample_db.sql
```

作成されるデータベースは、

```text
backup_test
```

です。

主なテーブルは次の2つです。

```text
users
orders
```

`orders.user_id` は、Foreign Keyで `users.id` を参照しています。

```text
users
  ↑
  │ Foreign Key
orders
```

そのため、テーブルの作成順序やリストア順序によってはエラーになることがあります。

---

# 2. サンプルデータについて

テストデータには、バックアップ時に注意が必要な値をあらかじめ含めています。

以下が正しくバックアップ・リストアできるか確認してください。

* 日本語
* NULL
* 空文字
* カンマ
* ダブルクォート
* 改行
* DATE
* DATETIME
* DATETIME(6)
* DECIMAL
* JSON
* Foreign Key

単に「エラーが出なかった」だけではなく、**バックアップ前とリストア後で値が同じか**を確認してください。

---

# 3. ★ MySQL接続

## Requirement 3-1

PythonからMySQLへ接続できること。

例えば、

```powershell
python main.py
```

を実行したときに、MySQLへの接続が成功することを確認します。

## Requirement 3-2

MySQLのバージョンを取得できること。

例：

```text
MySQL version: 8.4.x
```

実際のバージョン番号は環境によって異なって構いません。

## Requirement 3-3

`backup_test` 内のテーブル一覧を取得できること。

少なくとも、

```text
users
orders
```

が取得できること。

---

# 4. ★ テーブル定義のバックアップ

各テーブルのDDLを取得し、ファイルとして保存してください。

期待する構成例：

```text
backup-output/
└── schema/
    ├── users.sql
    └── orders.sql
```

## Requirement 4-1

`users.sql` が生成されること。

## Requirement 4-2

`orders.sql` が生成されること。

## Requirement 4-3

`users.sql` の内容に `CREATE TABLE` が含まれていること。

## Requirement 4-4

`orders.sql` の内容にForeign Keyの定義が含まれていること。

例えば、

```text
FOREIGN KEY
```

または、

```text
REFERENCES
```

に相当する内容が確認できること。

## Requirement 4-5

バックアップされたDDLを利用して、空のデータベース上にテーブルを再作成できること。

---

# 5. ★ データのCSVバックアップ

各テーブルのデータをCSVとして保存してください。

期待する構成例：

```text
backup-output/
├── schema/
│   ├── users.sql
│   └── orders.sql
└── data/
    ├── users.csv
    └── orders.csv
```

## Requirement 5-1

`users.csv` が生成されること。

## Requirement 5-2

`orders.csv` が生成されること。

## Requirement 5-3

`users` の3行が保存されていること。

## Requirement 5-4

`orders` の3行が保存されていること。

## Requirement 5-5

日本語が文字化けしていないこと。

例えば、

```text
田中 太郎
```

などの文字列が正しく保存されていること。

---

# 6. ★ CSV特殊文字

CSVでは、単純にカンマで文字列を連結するだけでは正しく保存できないデータがあります。

次の値が壊れずに扱えることを確認してください。

## Requirement 6-1 カンマ

次のような値を正しく保存・読み込みできること。

```text
東京, 横浜
```

または、

```text
定規, 30cm
```

カンマが列区切りとして誤認識されないこと。

## Requirement 6-2 ダブルクォート

次のような値を正しく保存・読み込みできること。

```text
鈴木 "花子"
```

または、

```text
ペン "太字"
```

## Requirement 6-3 改行

1つの値の中に改行が含まれていても、別のレコードとして扱われないこと。

サンプルデータには、

```text
1行目
2行目
```

という値が含まれています。

バックアップ後も1つのカラムの値として保持されることを確認してください。

---

# 7. ★ NULLと空文字

以下の2つは別の値です。

```text
NULL
```

と、

```text
""
```

です。

## Requirement 7-1

MySQLの `NULL` をCSVへ保存できること。

## Requirement 7-2

空文字をCSVへ保存できること。

## Requirement 7-3

バックアップからリストアした後も、

```text
NULL → NULL
空文字 → 空文字
```

となること。

例えば、`users.note` にはNULLと空文字の両方が含まれています。

### 注意

CSV上でNULLと空文字を両方とも、

```text
空欄
```

としてしまうと、リストア時に区別できなくなります。

どのような形式で保存するかは自分で考えてください。

---

# 8. ★ データ型

## Requirement 8-1 DATE

`birthday` が正しく保存・復元されること。

例：

```text
2000-01-01
```

## Requirement 8-2 DATETIME

`orders.created_at` が正しく保存・復元されること。

## Requirement 8-3 DATETIME(6)

マイクロ秒を含む値が失われないこと。

例：

```text
2026-09-01 09:00:00.123456
```

## Requirement 8-4 DECIMAL

次のような値が正しく保存・復元されること。

```text
92.50
500.00
120.00
```

特に、バックアップとリストアを繰り返したことで値が意図せず変化しないことを確認してください。

## Requirement 8-5 JSON

`orders.metadata` のJSONを保存できること。

NULLのJSONも扱えること。

---

# 9. ★ manifest.json

バックアップ内容を説明する `manifest.json` を作成してください。

期待する構成：

```text
backup-output/
├── schema/
├── data/
└── manifest.json
```

## Requirement 9-1

`manifest.json` が生成されること。

## Requirement 9-2

バックアップ対象のデータベース名が分かること。

例：

```json
{
  "database": "backup_test"
}
```

## Requirement 9-3

バックアップに含まれるテーブル一覧が分かること。

## Requirement 9-4

各テーブルについて、DDLファイルの場所が分かること。

## Requirement 9-5

各テーブルについて、データファイルの場所が分かること。

## Requirement 9-6

各テーブルのバックアップ行数が分かること。

期待値：

```text
users  : 3
orders : 3
```

---

# 10. ★ 大量データを意識した読み取り

本番環境では、テーブルに数百万行以上のデータが存在する可能性があります。

すべての行を一度にPythonのメモリへ読み込む設計になっていないか確認してください。

## Requirement 10-1

データを複数行ずつ取得する方法を検討していること。

例：

```text
1000行取得
↓
CSVへ書き込み
↓
次の1000行取得
```

## Requirement 10-2

テーブル全体を巨大なPythonリストとして保持する必要がない設計になっていること。

実際に数百万行のテストデータを準備する必要はありません。

**なぜその設計が大量データに向いているのか説明できればOKです。**

---

# 11. ★★ CLI

ソースコードを書き換えずに、コマンドライン引数から動作を指定できるようにしてください。

## Requirement 11-1

出力先を指定できること。

例：

```powershell
python main.py `
  --output .\backup-output
```

## Requirement 11-2

出力形式を指定できること。

例：

```powershell
python main.py `
  --output-type plain `
  --output .\backup-output
```

## Requirement 11-3

不正な引数が指定された場合に、利用者が原因を理解できるメッセージが表示されること。

---

# 12. ★★ テーブル選択バックアップ

## Requirement 12-1

特定のテーブルだけバックアップできること。

例：

```powershell
python main.py `
  --output-type plain `
  --output .\backup-output `
  --tables users
```

この場合、

```text
users
```

だけがバックアップされること。

## Requirement 12-2

複数テーブルを指定できること。

例：

```powershell
--tables users orders
```

## Requirement 12-3

`--tables` を指定しない場合、すべてのテーブルがバックアップされること。

## Requirement 12-4

存在しないテーブルが指定された場合、適切なエラーになること。

例：

```powershell
--tables not_exists
```

---

# 13. ★★ ZIPバックアップ

## Requirement 13-1

ZIP形式のバックアップを作成できること。

例：

```powershell
python main.py `
  --output-type zip `
  --output .\backup.zip
```

## Requirement 13-2

生成されたZIPを正常に開けること。

## Requirement 13-3

ZIP内部に次のような構造があること。

```text
schema/users.sql
schema/orders.sql
data/users.csv
data/orders.csv
manifest.json
```

## Requirement 13-4

ZIPが破損していないこと。

## Requirement 13-5

plain形式とZIP形式で、バックアップ対象データの意味が変わらないこと。

---

# 14. ★★ リストア

リストア先として、例えば次のデータベースを利用します。

```text
backup_restore_test
```

## Requirement 14-1

バックアップからテーブルを再作成できること。

## Requirement 14-2

CSVからデータを投入できること。

## Requirement 14-3

`users` をリストアした場合、3行復元されること。

## Requirement 14-4

バックアップ前とリストア後で、主要な値が一致すること。

特に、

* 日本語
* NULL
* 空文字
* カンマ
* ダブルクォート
* 改行
* DATE
* DATETIME
* DECIMAL

を確認してください。

---

# 15. ★★ 選択リストア

## Requirement 15-1

`users` だけをリストアできること。

例：

```powershell
python restore.py `
  --input-type zip `
  --input .\backup.zip `
  --database backup_restore_test `
  --tables users
```

期待する状態：

```text
users   → 存在する
orders  → 存在しない
```

## Requirement 15-2

指定していないテーブルが勝手にリストアされないこと。

---

# 16. ★★ 既存テーブルへの対応

同じバックアップを2回リストアすると、

```text
Table already exists
```

のような問題が発生する可能性があります。

どのような仕様にするか考えてください。

例えば、

```powershell
--drop-existing
```

のようなオプションを設ける方法があります。

## Requirement 16-1

既存テーブルがある場合の動作が明確であること。

## Requirement 16-2

利用者の意図なく既存データを削除しない設計になっていること。

---

# 17. ★★★ Foreign Key依存関係

`orders` は `users` に依存しています。

## Test 17-A

空のリストア先DBへ、

```text
users
orders
```

の順番で復元してください。

正常に復元できるか確認します。

## Test 17-B

次に、

```text
orders
users
```

の順番で復元してみてください。

何が起きるか確認してください。

### Requirement 17-1

なぜ結果が異なるのか説明できること。

### Requirement 17-2

Foreign Keyによる依存関係を取得する方法を調査できていること。

---

# 18. ★★★ manifestへの依存関係保存

manifestを拡張して、

```json
{
  "name": "orders",
  "dependsOn": [
    "users"
  ]
}
```

のような情報を保存することを検討してください。

## Requirement 18-1

`orders` が `users` に依存していることをmanifestから判断できること。

## Requirement 18-2

`users` に不要な依存先が登録されていないこと。

---

# 19. ★★★ トポロジカルソート

利用者が、

```text
orders
users
```

の順に指定しても、実際には、

```text
users
orders
```

の順で復元できるようにすることを考えます。

## Requirement 19-1

テーブルの依存関係から適切な復元順序を計算できること。

## Requirement 19-2

次の指定でも、

```powershell
--tables orders users
```

内部的には、

```text
users
orders
```

として復元されること。

## Requirement 19-3

必要な依存テーブルが指定されていない場合、分かりやすいエラーになること。

例：

```powershell
--tables orders
```

に対して、

```text
orders の復元には users が必要
```

という意味のエラーが出ること。

---

# 20. ★★★ 循環依存

例えば、

```text
A depends on B
B depends on A
```

という状態では、単純な順番を決めることができません。

## Requirement 20-1

循環依存を検出できること。

## Requirement 20-2

無限ループにならないこと。

## Requirement 20-3

利用者が原因を理解できるエラーメッセージになること。

循環依存を実際にリストアできるところまで実装する必要はありません。

---

# 21. ★★★ Amazon S3

## Requirement 21-1

Pythonから指定されたS3バケットへテストファイルをアップロードできること。

## Requirement 21-2

どのAWS認証情報を利用しているか確認できること。

例：

```powershell
aws sts get-caller-identity --profile <profile-name>
```

## Requirement 21-3

バックアップファイルをS3へ保存できること。

最初はローカルで作ったZIPをアップロードする方法でも構いません。

---

# 22. ★★★ S3 Multipart Upload

## Requirement 22-1

Multipart Uploadを開始できること。

## Requirement 22-2

複数のPartをアップロードできること。

## Requirement 22-3

すべてのPartを送信した後、Multipart UploadをCompleteできること。

## Requirement 22-4

途中でエラーになった場合、必要に応じてAbortできること。

## Requirement 22-5

完成したS3オブジェクトをダウンロードし、元データと一致することを確認できること。

---

# 23. ★★★ Streaming ZIP → S3

最終チャレンジです。

目標：

```text
MySQL
  ↓
CSV
  ↓
ZIP
  ↓
Multipart Upload
  ↓
Amazon S3
```

ローカルディスク上に完成版ZIPを作らず、ZIP生成とS3アップロードを並行して進めます。

## Requirement 23-1

ZIP全体をメモリに保持する必要がないこと。

## Requirement 23-2

ローカルに完成版ZIPを一時保存しなくてもS3へ保存できること。

## Requirement 23-3

S3からダウンロードしたZIPが正常に開けること。

## Requirement 23-4

ZIP内のファイル構成が通常のローカルZIPと同じであること。

## Requirement 23-5

ZIPの終了処理が完了してからMultipart UploadをCompleteしていること。

---

# 24. 異常系テスト

正常に動く場合だけでなく、エラー時の動作も確認してください。

可能な範囲で次を試します。

## MySQL

* MySQLが起動していない
* パスワードが間違っている
* DB名が間違っている
* 存在しないテーブルを指定

## File

* 出力先が存在しない
* 同名ファイルが存在する
* 書き込み権限がない

## Restore

* manifestが存在しない
* CSVが存在しない
* schemaファイルが存在しない
* 既存テーブルが存在する
* 必要な依存テーブルがない

## AWS

* AWS認証情報がない
* S3バケット名が間違っている
* `AccessDenied`
* Multipart Upload途中で例外が発生

すべて対応する必要はありません。

どのエラーを想定し、どのような対応を実装したか説明できるようにしてください。

---

# 25. 最終確認

最低限、次の流れを一度通してください。

```text
backup_test
    ↓
自作ツール
    ↓
バックアップ作成
    ↓
backup_restore_test
    ↓
リストア
    ↓
元データと比較
```

## 最終チェック

* [ ] MySQLへ接続できる
* [ ] テーブル一覧を取得できる
* [ ] DDLを保存できる
* [ ] CSVを保存できる
* [ ] manifestを作成できる
* [ ] NULLと空文字を区別できる
* [ ] 特殊文字を扱える
* [ ] リストアできる
* [ ] 元データと復元データが一致する

ここまでが基本ゴールです。

余裕があれば、

* [ ] ZIP
* [ ] CLI
* [ ] テーブル選択
* [ ] 選択リストア
* [ ] S3
* [ ] Multipart Upload
* [ ] Streaming ZIP
* [ ] Foreign Key依存関係
* [ ] トポロジカルソート

にも挑戦してください。

---

# 26. 発表時に説明できるようにすること

最終的には、コードだけではなく次の内容を説明できるようにしてください。

1. 今回作ったツールは何をするものか
2. mysqldumpとはどのようなツールか
3. 自作ツールのバックアップ形式
4. なぜDDLとCSVを分けたのか
5. manifestには何を保存したのか
6. NULLや特殊文字をどのように扱ったのか
7. 大量データに対してどのような工夫をしたか
8. AWS friendlyとは何を意味するか
9. 実装できなかった機能は何か
10. 今後改善するなら何をしたいか

**完成した機能の数だけでなく、設計・検証・調査の過程も成果です。**
