import mysql.connector
from mysql.connector import Error
import csv
import os
from pathlib import Path
from datetime import datetime
import json
import shutil
import zipfile


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

    #mysqldump保存
    for table in tables_list:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table};")

        sql_path = (
            Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/schema/')/ f"{table}.sql")

        with open(sql_path, "w", encoding="utf-8") as sqlfile:
            for row in cursor:
                values = []

                for value in row:
                    if value is None:
                        values.append("NULL")
                    elif isinstance(value, str):
                        values.append(f"'{value}'")
                    else:
                        values.append(str(value))

                sql = (f"INSERT INTO {table} VALUES "f"({', '.join(values)});\n")

                sqlfile.write(sql)
      
        print(f"{table}.sql を作成しました")

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
    "MySQL Version": "MySQL Version: " ,
    "ファイルサイズ": {f"{table}.csv": f"{os.path.getsize(Path(__file__).parent.parent / 'backup-output2' / 'data' / f'{table}.csv')} bytes"for table in tables_list },
    "データベース一覧": [database[0] for database in databases],


}
"""
for i in range(len(tables_list)):
cursor = connection.cursor()
cursor.execute(f"SELECT COUNT(*) FROM {tables_list[i]};")
row_count = cursor.fetchone()[0]
backup_info["tables"].append({
    "table_name": tables_list[i],
    "row_count": row_count
})
"""
#jsonファイルに書き込み
with open(Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/') / 'manifest.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(backup_info, jsonfile, ensure_ascii=False, indent=4)

print("バックアップ情報をJSONファイルに書き込みました。")


#zip化

def zip_directory(source_dir, output_zip):
    """
    :param source_dir: 圧縮したいディレクトリのパス
    :param output_zip: 出力ZIPファイルのパス
    """
    if not os.path.isdir(source_dir):
        raise ValueError(f"指定されたパスがディレクトリではありません: {source_dir}")

    # shutil.make_archiveは拡張子を自動で付与するらしい
    shutil.make_archive(output_zip, 'zip', root_dir=source_dir)
    print(f"ZIPファイルを作成しました: {output_zip}.zip")

#csv
directory_csv_path =  "C:/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2"

zip_file_csv_path = 'C:/Users/ssg/mysql-backuo-tool/mysql-backup'
print(zip_file_csv_path+"がパス")
"""
with zipfile.ZipFile(zip_file_csv_path, 'w') as zip_file:
    for root, dirs, files in os.walk(directory_csv_path):
        for file in files:
            file_path = os.path.join(root, file)
            zip_file.write(file_path, os.path.relpath(file_path, directory_csv_path))
"""
try:
    zip_directory( directory_csv_path,zip_file_csv_path )

except Error as e:
    print(f"エラー: {e}")


"""
#dump
directory_path_dump= "C:/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/schema"

zip_file_path ='C:/Users/ssg/mysql-backuo-tool/mysql-backup'
"""







