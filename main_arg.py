
# libraries
import argparse
from multiprocessing import Pool, cpu_count

# self-implementations
from backup_tool.mysql_source import MySQLSource
from backup_tool.config import load_mysql_config
from backup_tool.output_sql import SchemaExport

# command example below
# python .\main_arg.py backup_test -schema -db-password aaaa

def main():
    # definitions
    requirements = [ # name, description
        ["db_name", "target database name"],
    ]
    flags = [ # name, description
        ["-debug", "show debug massages"],
        ["-schema", "output schema with data"],
        ["-schema-no-data", "output schema with only structure info"],
    ]
    options = [ # name, default value, number of arg, description
        ["-db-password", "", None, ""],
        ["-output-types", "csv", "+", ""],
        ["-output-name", "output", None, ""],
    ]


    # initializes
    parser = argparse.ArgumentParser(
        description="""
mysql backup tool
descriptions
descriptions
descriptions""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    reqs_group = parser.add_argument_group("requirements")
    flags_group = parser.add_argument_group("flags")


    for requirement in requirements:
        parser.add_argument(
            requirement[0],
            help= requirement[1],
            
        )
    for flag in flags:
        flags_group.add_argument(
            flag[0],
            action= "store_true",
            help= flag[1],
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

    database_name = args.db_name
    password = args.db_password
    config = load_mysql_config()
    is_debug = args.debug
    
    if args.schema:
        schema_work = SchemaExport(
            database_name=database_name,
            password=password,
            config=config,
            is_debug=is_debug,
        )
        work.append(schema_work)
    elif args.schema_no_data:
        schema_work = SchemaExport(
            database_name=database_name,
            password=password,
            config=config,
            is_debug=is_debug,
            no_data=True,
        )
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

    n = cpu_count()
    with Pool(processes=n) as p:
        results = p.map(func, work)

def func(w: MySQLSource):
    w.do_output()

if __name__ == "__main__":
    main()