
# libraries
import argparse
from multiprocessing import Pool, cpu_count
#import time

# self-implementations
from backup_tool.mysql_source import MySQLSource
from backup_tool.config import load_mysql_config
from backup_tool.output_sql import SchemaExport

# command example below
# python .\main_arg.py -schema -output-types csv -settings-path settings.env

def main():
# definitions
    #requirements = [ # name, description
        #["db_name", "target database name"],
    #]
    flags = [ # name, description
        ["-debug", "show debug massages"],
        ["-schema", "output schema with data"],
        ["-schema-no-data", "output schema with only structure info"],
        ["-zip", "output in zipping"],
        ["-s3", "output into s3 (settings.env required)"],
    ]
    options = [ # name, default value, number of arg, description
        #["-db-password", "", None, "password of your database"],
        ["-db-tables", "", "+", "one or several specific table name you wanna backup"],
        ["-output-types", "csv", "+", "one or several plain file types you want \nby default: csv \ncan be: csv"],
        ["-directory", "./backup", None, "directory you wanna backup into \nby default: backup"],
        ["-settings-path", "settings.env", None, "you can set options via settings.env (or just you name it)"],
    ]


# initializes
    parser = argparse.ArgumentParser(
        description="""
mysql backup tool
set some parameters such as sql password, host or database name via settings.env
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    flags_group = parser.add_argument_group("flags")


    #for requirement in requirements:
    #    parser.add_argument(
    #        requirement[0],
    #        help= requirement[1],
    #    )
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


# processes
    is_debug = args.debug
    config = load_mysql_config(
        setting_file_path=args.settings_path,
        is_debug=is_debug
    )
    # judge whether each tables exist
    for_check_tables = MySQLSource(config=config)
    for_check_tables.connect()
    tables_exists = for_check_tables.list_tables()
    tables_ok = []

    if not args.db_tables:
        tables_ok = tables_exists
    else: 
        for t in args.db_tables:
            if t in tables_exists:
                tables_ok.append(t)
            else:
                print(f"the table {t} doesn't exist")
                print("you wanna continue without it?")
                ans = ""
                while not (ans == "y" or ans == "n"):
                    ans = input("y/n: ")
                match ans:
                    case "y":
                        print("yes")
                        continue
                    case "n":
                        print("no")
                        return None
                    case _: print("aaaaaaaaaaaaaaaaaaaaaa")
    for_check_tables.close()

    work: list[MySQLSource] = []
    # contain any backup process, called in multiprocessing
    # must be given instances of class which extends from MySQLSource
    # but the class must recieve 1 table name
    # 1 instance for 1 table thus multiprocessing for each tables

    # whether do schema
    if args.schema:
        for t in tables_ok:
            schema_work = SchemaExport(
                config=config,
                table=t,
            )
            work.append(schema_work)
    elif args.schema_no_data:
        for t in tables_ok:
            schema_work = SchemaExport(
                config=config,
                table=t,
            )
            work.append(schema_work)
    else: None

    # whether do plains
    plain = args.output_types
    if type(plain) == type(""):
        print(plain)
    elif type(plain) == type([]):
        for p in plain:
            match p:
                case "csv" | ".csv":
                    # TODO implement csv process here
                    pass
                #case "txt" | ".txt":
                    # todo implement txt process here
                #    pass
                case _:
                    print("error: invalid value on output types")
    else:
        print("error: invalid value on output types")



    # any work's element executed here
    n = cpu_count()
    with Pool(processes=n) as p:
        results = p.map(func, work)
    #for w in work:
    #    func(w=w)

    if args.zip:
        # TODO zip function here
        pass
    

def func(w: MySQLSource):
    w.connect()
    w.do_output()
    w.close()

if __name__ == "__main__":
    #start = time.perf_counter()
    main()
    #end = time.perf_counter()

    #print(end - start)