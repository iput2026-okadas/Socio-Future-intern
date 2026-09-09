
# libraries
import argparse


# self-implementations
from backup_tool.mysql_source import MySQLSource
from backup_tool.config import load_mysql_config
from backup_tool.output_sql import SchemaExport
# definitions
requirements = [
    "db-name"
]
flags = [
    ["-debug", "show debug massages"],
    ["-schema", "whether try to output schema"]
]
options = [
    ["-db-password", "", None, ""],
    ["-output-types", "csv", "+", ""],
    ["-output-name", "output", None, ""],
]

# main

# initialize
parser = argparse.ArgumentParser()

for requirement in requirements:
    parser.add_argument(
        requirement
    )
for flag in flags:
    parser.add_argument(
        flag[0],
        action= "store_true",
        help= flag[1]
    )
for option in options:
    parser.add_argument(
        option[0],
        default= option[1],
        nargs= option[2],
        help= option[3],
    )

args = parser.parse_args()

print(args)


# process
work: list[MySQLSource] = []

config = load_mysql_config()
is_debug = args.debug

if args.schema:
    schema_work = SchemaExport(config=config, is_debug=is_debug)
    work.append(schema_work)
else: None


plain = args.output_types
if type(plain) == type(""):
    print(plain)
elif type(plain) == type([]):
    for p in plain:
        match p:
            case "csv" | ".csv":
                print("csv")
            case "txt" | ".txt":
                print("txt")
            case _:
                print("error: invalid value on output types")
else:
    print("error: invalid value on output types")



# any work's element executed here

for w in work:
    w.do_output()