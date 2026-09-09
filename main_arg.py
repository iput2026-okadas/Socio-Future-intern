
# libraries
import argparse


# self-implementations
from backup_tool.mysql_source import MySQLSource

# definitions
requirements = [
    "db-name"
]
options = [
    ["-schema", "y", None, "whether try to output schema -- y/n"],
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

if s := args.schema:
    if s == "y" or s == "yes":
        work.append("schema")
        # schema
    elif s == "n" or s == "no":
        None
    else:
        print("error: schema option is yes or no")


plain = args.output_types
if type(plain) == type(""):
    print(plain)
elif type(plain) == type([]):
    for p in plain:
        match p:
            case "csv" | ".csv":
                work.append("csv")
            case "txt" | ".txt":
                work.append("txt")
            case _:
                print("error: invalid value on output types")
else:
    print("error: invalid value on output types")




print(work)

# any work's element executed here