
# libraries
from decimal import Decimal
from datetime import datetime, date, time, timedelta

# self-implementations
from backup_tool.mysql_source import MySQLSource

class SchemaExport(MySQLSource):

    def __init__(
            self,
            database_name: str,
            password: str,
            config,
            is_debug,
            no_data=False,
        ):
        super().__init__(
            database_name,
            password,
            config,
            is_debug,
        )
        self.no_data = no_data
    
    def do_output(self):

        self.connect()
        
        for s in self.list_tables():
            self.debug(f"parse table: {s} into .sql")
            with open(
                f"backup-output2/schema/{s}.sql",
                "w", encoding='utf-8'
            ) as f:
                f.write("\n")

                f.write(f"DROP TABLE IF EXISTS {s};\n")
                f.write(create_table := self.get_create_table(s)[0][1])

                f.write(f";\n")
                f.write(f"\n")

                self.debug(column_types := self.get_column_types(s))

                
                if not self.no_data:
                    f.write(f"LOCK TABLES {s} WRITE;\n")
                    for it in self.iter_row_batches(s):
                        insert = f"INSERT INTO {s} VALUES("

                        for index, i in enumerate(it):
                            if i == None:
                                insert = insert + "NULL"
                            elif isinstance(i, (int, float, bytes, bytearray, Decimal)):
                                insert = insert + str(i)
                            elif isinstance(i, (datetime, date, time, timedelta)):
                                insert = insert + "\'" + str(i) + "\'"
                            else:
                                insert = insert + repr(i)

                            if not index == len(it) - 1:
                                insert = insert + ","
                        insert = insert + ");\n"

                        f.write(insert)
                    f.write(f"UNLOCK TABLES;\n")
