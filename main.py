import argparse
import logging
import os
import sys
import json
import base64
from datetime import datetime
from db_access import Database, InfoDataModel

def tool_arguments():
    parser = argparse.ArgumentParser(
        description="Store your passwords in a fancy way.", 
        prog="storepass",
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
    view_parser.add_argument("-s","--search", 
                             metavar="<keyword>", 
                             help="Query information based on provided keyword."
                             )
    view_parser.add_argument("-l","--limit",
                             metavar="<number>",
                             type=int,
                             default=5,
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
    site = input("site: ")
    username = input("username: ")
    password = input("password: ")
    
    others = input("do you want to input other fields? (y/n) ")
    
    if others.lower() == "y":
        # TODO: add additional information to be inputted.
        pass

    curr_date = datetime.now().strftime("%d:%m:%YT%H:%M:%S")

    info_data = InfoDataModel(site, username, password, curr_date)

    database.insert_data(info_data)
    sys.exit(0)
    
def view_data(database: Database, args: argparse.Namespace):
    database.get_all_info(limit=args.limit)
    sys.exit(0)
    
def main(args : argparse.Namespace):
    db = Database()
    
    logging.debug(f"Arguments: {args}")

    if args.cmd == "add":
        add_data(db)
    elif args.cmd == "view":
        view_data(db, args)
    elif args.cmd == "rmv":
        print("remove data")

def init_logging():
    log_dir = os.getcwd() + "/logs/"
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