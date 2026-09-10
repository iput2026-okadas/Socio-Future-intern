import mysql.connector
from mysql.connector import Error
import csv
import os
from pathlib import Path
from datetime import datetime
import json

# 接続設定
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0426',
    'charset': 'utf8mb4'
}

try:
    # 接続
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("USE backup_test;")
   

    #テーブル一覧表示
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    
    tables_list = []
    for table in tables:
        tables_list.append(table[0])
        print("テーブル名:", table[0]+"\n")
    cursor.close()

    #テーブル指定を自動化するためにリストを使用し割り当てる
    tables_numbers = len(tables_list)


    #カラム一覧表示
    for i in range(len(tables_list)):
        cursor = connection.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {tables_list[i]};")
        columns = cursor.fetchall()
        print(f"{tables_list[i]}のカラム一覧:")
        for column in columns:
            print(column[0])
        print("\n")
    cursor = connection.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {tables_list[len(tables_list)-1]};")
    columns = cursor.fetchall()
    print(f"{tables_list[len(tables_list)-1]}のカラム一覧:")
    for column in columns:
        print(column[0])


    # csvファイルに書き込み

    for i in range(len(tables_list)):
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {tables_list[i]};")
        with open( Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/data/')/f"{tables_list[i]}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([p[0] for p in cursor.description]) 
            for row in cursor:
                writer.writerow(row)  
        print(f"{tables_list[i]}テーブルのデータをCSVファイルに書き込みました。")   

except Error as e:
    print(f"エラー: {e}")


# jsonファイルに書き込み
"""
以下、バックアップの内容を説明するためのjsonファイルを作成するコード
注意:上記にてテーブル指定を自動化するためにリストを使用しているので、テーブル名を直接指定する必要はありません。
"""
#データベース一覧表示
cursor.execute("SHOW DATABASES;")
databases = cursor.fetchall()
print("データベース一覧:")
for database in databases:
    print(database[0])

    
#バックアップ情報を格納する辞書を作成
backup_info = {
    "テーブルリスト": tables_list,
    "tables": [],
    "バックアップ日時:": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "MySQL Version": "MySQL Version: " + connection.get_server_info(),
    "ファイルサイズ": {f"{table}.csv": f"{os.path.getsize(Path(__file__).parent.parent / 'backup-output2' / 'data' / f'{table}.csv')} bytes"for table in tables_list },
    "データベース一覧": [database[0] for database in databases],


}

"""    # MySQLのバージョン取得
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    #cursor.fetchone():SQLクエリの結果をすべて取得し、リスト形式で返す
    print("Mysql Version:", version[0],"\n")

    #日時表示
    print("バックアップ日時:", datetime.now().strftime("%Y-%m-%d"),"/n")

    #csvのファイルサイズ取得
    for table in tables_list:
        csv_path = (
            Path(__file__).parent.parent/ "backup-output2"/ "data"/ f"{table}.csv"
        )

        size = os.path.getsize(csv_path)

        print(f"{table}.csv : {size} bytes")"""



for i in range(len(tables_list)):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tables_list[i]};")
    row_count = cursor.fetchone()[0]
    backup_info["tables"].append({
        "table_name": tables_list[i],
        "row_count": row_count
    })

#jsonファイルに書き込み
with open(Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/') / 'manifest.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(backup_info, jsonfile, ensure_ascii=False, indent=4)

print("バックアップ情報をJSONファイルに書き込みました。")