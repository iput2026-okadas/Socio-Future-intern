import mysql.connector
from mysql.connector import Error
import csv
import os
from pathlib import Path

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

    """fetchall
    ・検証パターンで一番早い
    ・全てのデータをPython実行端末にもってくるので、取得データ分メモリを使用する
    ・pythonコードを書くとき、 fetchall() して ループするだけでいいのでコードは簡単
    ・arraysize によるチューニングする余地はある（どの値が適切かは環境依存）

    fetchmany

    ・検証パターンは２番目に早い
    ・arrayseizeで指定した分のデータをPython実行端末にもってくるので、データ取得で使用するデータ量に依存せず、使用するメモリ量は一定。
    ・pythonコードを書くとき、 fetchall() よりも若干コードが増える
    ・arraysize によるチューニングする余地はある（どの値が適切かは環境依存）

    fetchone
    ・検証パターンは３番目
    ・1件ずつデータをPython実行端末にもってくるので、データ取得で使用するメモリ量は少ない。
    ・pythonコードを書くとき、 fetchall() よりも若干コードが増える"""


    cursor.execute("USE backup_test;")
   

    #テーブル一覧表示
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("テーブル一覧:")
    for table in tables:
        print(table[0])
    print("\n")
    cursor.close()

    #ordersカラム一覧表示
    cursor = connection.cursor()
    cursor.execute("SHOW COLUMNS FROM orders;")
    columns = cursor.fetchall()
    print("ordersのカラム一覧:")
    for column in columns:
        print(column[0])

   #ordersテーブルに何行あるかを表示
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders;")
    count = cursor.fetchone()
    print("ordersの行数:", count[0],"\n")

    #userカラム一覧表示
    cursor = connection.cursor()
    cursor.execute("SHOW COLUMNS FROM users;")
    columns = cursor.fetchall()
    print("usersのカラム一覧:")
    for column in columns:
        print(column[0])


    #usersテーブルに何行あるかを表示
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()
    print("usersの行数:", count[0],"\n")

    #テーブルデータSELECT
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders;")
    print("ordersテーブルのデータ:")

    #order csvファイルに書き込み
    with open( Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/data/')/'orders.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cursor.description]) 
        for row in cursor:
            writer.writerow(row)    

    #users csvファイルに書き込み
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    print("usersテーブルのデータ:")
    with open( Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/data/')/'users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cursor.description]) 
        for row in cursor:
            writer.writerow(row)
    """ 
   df = pd.read_csv('C:\\Users\\ssg\\mysql-backuo-tool\\mysql-backup\\orders.csv')
    df.to_csv('C:\\Users\\ssg\\mysql-backuo-tool\\mysql-backup\\orders_backup.csv', index=False)"""
    """
    os.chdir('C://') 

    #相対パスでCSVファイルを読み込む
    df = pd.read_csv('renshuu/renshuu.csv')
    df
    """


except Error as e:
    print(f"エラー: {e}")
