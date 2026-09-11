
# libraries
from decimal import Decimal
from datetime import datetime, date, time, timedelta

# self-implementations
from backup_tool.mysql_source import MySQLSource

class SchemaExport(MySQLSource):

    def __init__(
            self,
            config,
            table,
            no_data=False,
        ):
        super().__init__(
            config,
        )
        self._table = table
        self._no_data = no_data
    
    def do_output(self):

        self.debug(f"parse table: {self._table} into .sql")
        with open(
            f"backup-output2/schema/{self._table}.sql",
            "w", encoding='utf-8'
        ) as f:
            f.write("\n")

            f.write(f"DROP TABLE IF EXISTS {self._table};\n")
            f.write(create_table := self.get_create_table(self._table)[0][1])

            f.write(f";\n")
            f.write(f"\n")

            self.debug(column_types := self.get_column_types(self._table))

            if not self._no_data:
                f.write(f"LOCK TABLES {self._table} WRITE;\n")
                for raw_iter in self.iter_row_batches(self._table):
                    self.debug(raw_iter)
                    for it in raw_iter:
                        insert = f"INSERT INTO {self._table} VALUES("

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
