
# libraries
import argparse
from multiprocessing import Pool, cpu_count

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
        ["-output-types", "csv", "+", "one or several plain file types you want \nby default: csv \ncan be: csv"],
        ["-directory", "./backup", None, "directory you wanna backup into \nby default: backup"],
        ["-settings-path", "settings.env", None, "you can set options via settings.env (or just you name it)"],
    ]


    # initializes
    parser = argparse.ArgumentParser(
        description="""
mysql backup tool
set some parameters like sql password, host or database name via settings.env
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


    # process
    work: list[MySQLSource] = []

    config = load_mysql_config(
        setting_file_path=args.settings_path
    )
    is_debug = args.debug
    
    if args.schema:
        schema_work = SchemaExport(
            config=config,
            is_debug=is_debug,
        )
        work.append(schema_work)
    elif args.schema_no_data:
        schema_work = SchemaExport(
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
                    # TODO implement csv process here
                    pass
                #case "txt" | ".txt":
                    # TODO implement txt process here
                #    pass
                case _:
                    print("error: invalid value on output types")
    else:
        print("error: invalid value on output types")



    # any work's element executed here
    n = cpu_count()
    with Pool(processes=n) as p:
        results = p.map(func, work)

    if args.zip:
        # TODO zip function here
        pass
    

def func(w: MySQLSource):
    w.do_output()

if __name__ == "__main__":
    main()