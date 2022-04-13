import argparse
import logging
import os
import sys
from datetime import datetime
from db_access import Database, InfoDataModel

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def arguments():
    parser = argparse.ArgumentParser(
        description="Store and access your passwords in a fancy way.", 
        prog="mypass",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    sub_parser = parser.add_subparsers(
        dest="cmd", 
        help="Actions",
        )
    
    add_parser = sub_parser.add_parser("add", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    view_parser = sub_parser.add_parser("view", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    search_parser = sub_parser.add_parser("search", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rmv_parser = sub_parser.add_parser("rm", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # view cmd
    view_grp_parser = view_parser.add_mutually_exclusive_group(required=True)
    view_grp_parser.add_argument("-r","--ref",
                             type=str,
                             metavar="REFERENCE", 
                             help="Show full detail of the data.",
                             )
    view_grp_parser.add_argument("-a","--all",
                             help="Show brief detail of all data.",
                             action='store_true'
                             )
    view_parser.add_argument("--limit",
                             metavar="NUMBER",
                             type=int,
                             default=3,
                             help="Total number of data to be display."
                             )
    view_parser.add_argument("--offset",
                             metavar="NUMBER",
                             type=int,
                             default=0,
                             help="Starting number of data to be display."
                             )
    # search cmd
    
    search_parser.add_argument("-n","--name",
                             metavar="KEYWORD", 
                             help="Search for data by name."
                             )
    search_parser.add_argument("-u","--username",
                             metavar="KEYWORD", 
                             help="Search for data by username."
                             )
    search_parser.add_argument("-p","--password",
                             metavar="KEYWORD", 
                             help="Search for data by password."
                             )
    search_parser.add_argument("--limit",
                             metavar="NUMBER",
                             type=int,
                             default=3,
                             help="Total number of data to be display."
                             )
    search_parser.add_argument("--offset",
                             metavar="NUMBER",
                             type=int,
                             default=0,
                             help="Starting number of data to be display."
                             )
    # remove cmd
    rmv_grp_parser = rmv_parser.add_mutually_exclusive_group(required=True)
    rmv_grp_parser.add_argument("-r","--ref",
                            metavar="REFERENCE",
                            help="Remove the data from database."
                            )
    rmv_grp_parser.add_argument("-a","--all",
                            help="Clear all stored data",
                            action='store_true'
                            )
    
    args = parser.parse_args()
   
    # error traps
    if len(sys.argv) == 1 and args.cmd is None:
        parser.print_help(sys.stderr)
        sys.exit()
            
    if len(sys.argv) == 2 and args.cmd == "rmv":
        rmv_parser.print_help(sys.stderr)
        sys.exit()
    
    if args.cmd == "search" and not (args.name or args.username or args.password):
        search_parser.error("one of the argument is required -n/--name, -u/--username, or -p/-password")
        sys.exit()
        
    return args

def add_data(database: Database):
    name = input("name: ")
    username = input("username/email: ")
    password = input("password: ")
    
    others = input("do you want to input other fields? (y/n) ")
    
    curr_date = datetime.now().strftime("%d:%m:%YT%H:%M:%S")

    info_data = InfoDataModel(
        name=name, 
        username=username, 
        password=password, 
        created_at=curr_date
        )

    
    if others.lower() == "y":
        other_fields = {}

        print("Insert new fields.")
        while True:
            field = input("field: ")
            value = input(f"value ({field}): ")
            print()
            other_fields[field] = value
            is_done = input("Add another field? (y/n) ")

            if is_done.lower() != 'y':
                break
            
            print()
        logging.debug("Other fields {0}".format(other_fields))
        for field, value in other_fields.items():
            database.insert_other_info_data((info_data.ref, field, value))

    database.insert_info_data(info_data)

    database.commit()
    
    print("\nInserted new data with reference no: {0}".format(info_data.ref))
    sys.exit(0)
    
def view_data(database: Database, args: argparse.Namespace):
    if args.ref is None:
        database.get_all_info(limit=args.limit, offset=args.offset)
        print("\nTo show full detail of the information. \nUse `mypass view -r <reference#>`.\n")
    elif args.ref is not None:
        database.get_info(ref_no=args.ref)
    sys.exit(0)

def rmv_data(database: Database, args: argparse.Namespace):
    if args.ref is not None and not args.all :
        database.remove_data(args.ref)
        database.commit()
        print(f"Reference {args.ref} remove successfully.")
    elif args.all:
        database.remove_all()
        database.commit()
        print("Database cleared.")
        
    sys.exit(0)
    
def search_data(database: Database, args: argparse.Namespace):
    database.filter_info(name=args.name, username=args.username, password=args.password)
    print("\nTo view full detail of the information.\nUse `mypass view -r/--ref <reference>`.")
    database.close()
    sys.exit(0)
    
def main(args : argparse.Namespace):
    db = Database()
    
    logging.debug(f"Arguments: {args}")

    if args.cmd == "add":
        try:
            add_data(db)
        except KeyboardInterrupt:
            print("\nProcess interrupted.")
            sys.exit(1)
    elif args.cmd == "view":
        view_data(db, args)
    elif args.cmd == "search":
        search_data(db, args)
    elif args.cmd == "rm":
        rmv_data(db, args)

def init_logging():
    log_dir = ROOT_DIR + "/logs/"
    log_filename = datetime.now().strftime("%Y_%m_%d") + ".log"
    logging.basicConfig(
        filename=log_dir + log_filename,
        filemode='a',
        level=logging.DEBUG,
        format='%(asctime)s : [%(levelname)s] > %(message)s',
        datefmt='%I:%M:%S %p'
    )

if __name__ == "__main__":
    init_logging()
    args = arguments()
    main(args)