# MySQL Backup Tool

MySQLのデータを、テーブル単位で柔軟にバックアップ・リストアするためのPython製ツールです。

`mysqldump`よりもバックアップ内容を扱いやすくし、AWS S3へのストリーミングバックアップにも対応することを目的としています。

## 特徴

- テーブル構造とデータを分離してバックアップ
- バックアップ対象テーブルを選択可能
- 必要なテーブルだけを選択してリストア可能
- ローカルディレクトリへのplain出力
- ローカルZIP出力
- Amazon S3へのZIP直接出力
- S3 Multipart Upload対応
- ZIPをローカルに作成せず、ストリーミングでS3へアップロード
- 外部キーの依存関係をバックアップ時に保存
- リストア時に依存関係を考慮して復元順序を自動決定
- 大量データを想定したバッチ処理

---

## 背景

一般的なMySQLバックアップツールである`mysqldump`では、テーブル定義やデータなどがSQLとして出力されます。

本ツールでは、バックアップ内容をより扱いやすくするため、次のような構成で保存します。

```text
backup/
├── schema/
│   ├── users.sql
│   └── orders.sql
├── data/
│   ├── users.csv
│   └── orders.csv
└── manifest.json
```

テーブル構造はSQL、データはCSVとして分離します。

これにより、バックアップ後にテーブル単位で内容を確認したり、必要なテーブルだけを選択してリストアしたりできます。


---

# セットアップ

## 必要環境

- Python 3
- MySQL 8.x
- AWSアカウント（S3出力を利用する場合のみ）

## 仮想環境

Windows PowerShellの場合:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

依存パッケージをインストールします。

```powershell
python -m pip install -r requirements.txt
```

---

# 環境変数

プロジェクト直下に`.env`を作成します。

例:

```dotenv
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=backup_test
MYSQL_BATCH_SIZE=1000

AWS_PROFILE=your-aws-profile
S3_REGION=ap-northeast-1
S3_BUCKET=your-backup-bucket
```

AWS関連の設定は、`s3-zip`を使用する場合のみ必要です。

`.env`には認証情報に関係する設定が含まれるため、Gitへコミットしないでください。

---

# AWS認証

S3出力では、`.env`の`AWS_PROFILE`で指定されたAWS CLIプロファイルを使用します。

プロファイルの確認例:

```powershell
aws sts get-caller-identity `
  --profile your-aws-profile
```

S3へのバックアップには、対象バケットへの必要なS3権限が必要です。


---

# データ形式

テーブル定義は`SHOW CREATE TABLE`から取得し、SQLファイルとして保存します。

データはCSVとして保存します。

以下のような値も区別してバックアップ・リストアできるようにしています。

- NULL
- 空文字
- 改行を含む文字列
- カンマを含む文字列
- ダブルクォートを含む文字列
- 日本語
- DATE / DATETIME
- DECIMAL
- バイナリデータ

例えばNULLはCSV上で専用の表現を使用し、空文字と区別します。


---

# 主なファイル

```text
mysql-backup/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── sql/
│   └── setup_sample_db.sql
│
├── backup_tool/
│   ├── __init__.py
│   ├── config.py
│   └── mysql_source.py
│
├── main.py
│
└── tests/
    └── test_requirements.md
```
