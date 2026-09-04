from backup_tool.config import load_mysql_config
from backup_tool.mysql_source import MySQLSource


def main():
    config = load_mysql_config()

    with MySQLSource(config) as source:
        print("MySQL connection OK")
        print(f"MySQL version: {source.get_server_version()}")

        print()
        print("Tables:")
        for table_name in source.list_tables():
            print(f"- {table_name}")


if __name__ == "__main__":
    main()