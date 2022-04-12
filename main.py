import argparse
import logging
import os
import sys
import json
from datetime import datetime
from db_access import Database, InfoDataModel

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def tool_arguments():
    parser = argparse.ArgumentParser(
        description="Store your passwords in a fancy way.", 
        prog="mypass",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    sub_parser = parser.add_subparsers(
        dest="cmd", 
        help="Actions",
        )
    
    add_parser = sub_parser.add_parser("add", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    view_parser = sub_parser.add_parser("view", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rmv_parser = sub_parser.add_parser("rmv", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # view cmd
    view_parser.add_argument("-r","--ref",
                             metavar="<reference>", 
                             help="Show detail information of the reference."
                             )
    view_parser.add_argument("-s","--search",
                             metavar="<keyword>", 
                             help="Query information based on provided keyword."
                             )
    view_parser.add_argument("-l","--limit",
                             metavar="<number>",
                             type=int,
                             default=3,
                             help="Number of information to display."
                             )
    
    args = parser.parse_args()
   
    # error traps
    if len(sys.argv) == 1 and args.cmd is None:
        parser.print_help(sys.stderr)
        sys.exit()
            
    if len(sys.argv) == 2 and args.cmd == "rmv":
        rmv_parser.print_help()
        sys.exit()
        
    return args

def parse_dict_to_json(data:dict):
    return json.dumps(data)

def add_data(database: Database):
    name = input("name: ")
    username = input("username: ")
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
    database.close()
    sys.exit(0)
    
def view_data(database: Database, args: argparse.Namespace):
    if args.ref is None:
        print("To show detail information of a reference. \nUse `mypass view -r <reference>`.")
        database.get_all_info(limit=args.limit)
    else:
        database.get_info(ref_no=args.ref)

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
    elif args.cmd == "rmv":
        print("remove data")

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
    args = tool_arguments()
    main(args)