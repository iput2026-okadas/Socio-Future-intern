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

   

    #order csvファイルに書き込み
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders;")
    with open( Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/data/')/'orders.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        """
        len_orders = cursor.fetchall()
        
         for row in len_orders:
            writer.writerow(row)
            
        if len(len_orders) == 0:
            writer.writerow(["データなし"])
            len_orders = len_orders + 1
        else:"""
        writer.writerow([i[0] for i in cursor.description]) 
        for row in cursor:
            writer.writerow(row)  

    for col in cursor.description:
        print("coll:" + col[0])
        

    print(cursor.description)  

    #users csvファイルに書き込み
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    print("usersテーブルのデータ:")
    with open( Path('/Users/ssg/mysql-backuo-tool/mysql-backup/backup-output2/data/')/'users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cursor.description]) 
        for row in cursor:
            writer.writerow(row)

    #usersテーブルのカラム名を表示
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    print("usersテーブルのデータ:")
    for row in rows:
        print(row)

    #ordersテーブルのカラム名を表示
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")

    rows = cursor.fetchall()

    print("ordersテーブルのデータ:")
    for row in rows:
        print(row)

    


except Error as e:
    print(f"エラー: {e}")