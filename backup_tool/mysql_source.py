from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from backup_tool.config import MySQLConfig


Row = tuple[Any, ...]
RowBatch = list[Row]


class MySQLSource:
    """
    MySQLからバックアップ対象情報を読み取るクラス。

    このクラスはデータの取得だけを担当し、
    CSV、ZIP、S3への出力は担当しない。
    """

    def __init__(
            self,
            config: MySQLConfig,
            is_debug: bool,
        ) -> None:
        self._config = config
        self._is_debug = is_debug
        self._connection: MySQLConnection | None = None

    @property
    def database_name(self) -> str:
        """接続対象のデータベース名を返す。"""
        return self._config.database

    def connect(self) -> None:
        """MySQLへ接続する。"""
        if self._connection is not None:
            return

        self._connection = mysql.connector.connect(
            host=self._config.host,
            port=self._config.port,
            user=self._config.user,
            password=self._config.password,
            database=self._config.database,
            charset="utf8mb4",
            use_unicode=True,
            autocommit=False,
        )

    def close(self) -> None:
        """MySQL接続を閉じる。"""
        if self._connection is None:
            return

        if self._connection.is_connected():
            self._connection.close()

        self._connection = None

    def __enter__(self) -> "MySQLSource":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()

    def ping(self) -> None:
        """
        接続が利用可能か確認する。

        切断されている場合は再接続を試みる。
        """
        connection = self._require_connection()
        connection.ping(
            reconnect=True,
            attempts=3,
            delay=1,
        )

    def get_server_version(self) -> str:
        """MySQLサーバーのバージョンを取得する。"""
        connection = self._require_connection()

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT VERSION()")
            row = cursor.fetchone()

            if row is None:
                raise RuntimeError(
                    "MySQLバージョンを取得できませんでした。"
                )

            return str(row[0])
        finally:
            cursor.close()

    def list_tables(self) -> list[str]:
        """
        現在のデータベースにある通常テーブルの一覧を取得する。

        ビューは除外する。
        """
        connection = self._require_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SHOW FULL TABLES")

            tables: list[str] = []

            for row in cursor:
                table_name = str(row[0])
                table_type = str(row[1])

                if table_type == "BASE TABLE":
                    tables.append(table_name)

            return sorted(tables)
        finally:
            cursor.close()

    def get_create_table(self, table_name: str) -> str:
        """
        指定テーブルのCREATE TABLE文を取得する。

        Args:
            table_name: 取得対象のテーブル名。

        Returns:
            CREATE TABLE文。
        """
        connection = self._require_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"SHOW CREATE TABLE {table_name};")
            s = cursor.fetchall()
            return s
        finally:
            cursor.close()

    def get_columns(
        self,
        table_name: str,
    ) -> list[str]:
        """
        DESCRIBE結果をすべて返す
        """
        connection = self._require_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"DESCRIBE {table_name};")
            s = cursor.fetchall()
            return s
        finally:
            cursor.close()

    def get_column_types(
        self,
        table_name: str,
    ) -> list[str]:
        """
        DESCRIBEから型のみ取得
        """
        connection = self._require_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"DESCRIBE {table_name};")
            s = [column[1] for column in cursor.fetchall()]
            return s
        finally:
            cursor.close()

    def get_column_names(
        self,
        table_name: str,
    ) -> list[str]:
        """
        SELECT結果のdescriptionからカラム名を取得する。

        この段階では型情報の完全な復元には使用せず、
        CSVヘッダー候補となるカラム名だけを取得する。
        """

        connection = self._require_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"DESCRIBE {table_name};")
            s = [column[0] for column in cursor.fetchall()]
            return s
        finally:
            cursor.close()

    def iter_row_batches(
        self,
        table_name: str,
        batch_size: int | None = None,
    ) -> Iterator[RowBatch]:
        """
        指定テーブルのデータを一定件数ずつ取得する。

        全行を一度にメモリへ読み込まず、
        fetchmany()で分割して返す。

        Args:
            table_name: 対象テーブル名。
            batch_size: 1回に取得する最大件数。
                省略時は設定ファイルの値を使用する。

        Yields:
            行データのリスト。
        """

        connection = self._require_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"SELECT * FROM {table_name};")
            s = cursor.fetchall()
            return s
        finally:
            cursor.close()


    def count_rows(self, table_name: str) -> int:
        """
        動作確認用にテーブルの行数を取得する。

        実際のバックアップ処理では、
        別途COUNT(*)すると負荷が増えるため、
        書き出した件数を数える方法へ変更する予定。
        """
        self._validate_table_name(table_name)

        connection = self._require_connection()
        cursor = connection.cursor()

        quoted_name = self._quote_identifier(table_name)

        try:
            cursor.execute(
                f"SELECT COUNT(*) FROM {quoted_name}"
            )

            row = cursor.fetchone()

            if row is None:
                raise RuntimeError(
                    f"行数を取得できませんでした: "
                    f"{table_name}"
                )

            return int(row[0])
        finally:
            cursor.close()

    def _require_connection(self) -> MySQLConnection:
        """接続済みのMySQLConnectionを返す。"""
        if self._connection is None:
            raise RuntimeError(
                "MySQLへ接続されていません。"
                "connect()を先に実行してください。"
            )

        if not self._connection.is_connected():
            raise RuntimeError(
                "MySQLとの接続が切断されています。"
            )

        return self._connection

    def _validate_table_name(
        self,
        table_name: str,
    ) -> None:
        """
        指定されたテーブルが実在することを確認する。

        テーブル名はSQLパラメーターとして渡せないため、
        実在するテーブル一覧との照合を行う。
        """
        if not table_name:
            raise ValueError(
                "テーブル名が空です。"
            )

        existing_tables = self.list_tables()

        if table_name not in existing_tables:
            raise ValueError(
                f"指定されたテーブルは存在しません: "
                f"{table_name}"
            )

    @staticmethod
    def _quote_identifier(identifier: str) -> str:
        """
        MySQL識別子をバッククォートで囲む。

        事前に実在テーブルとの照合を行うことを前提とする。
        """
        escaped = identifier.replace("`", "``")
        return f"`{escaped}`"

    def get_table_dependencies(
        self,
        table_name: str,
    ) -> list[str]:
        """
        指定テーブルが外部キーで参照している
        親テーブル一覧を取得する。

        例:
            orders.user_id -> users.id

            orders の結果:
            ["users"]

        同一DB内の依存関係のみを対象とする。
        """
        # TODO: INFORMATION_SCHEMA.KEY_COLUMN_USAGE を使って実装してください
        pass

<<<<<<< HEAD

    def debug(self, s):
        if self._is_debug:
            print(s)


    def do_output():
        print()
=======
 
>>>>>>> 610a7ac4ccc7394caf64dd52f7c2a4e165a03ae5
