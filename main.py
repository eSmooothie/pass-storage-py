import argparse
import os
import sys
import json
import base64

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
    
    if len(sys.argv) == 2 and args.cmd == "view":
        view_parser.print_help()
        sys.exit()
        
    if len(sys.argv) == 2 and args.cmd == "rmv":
        rmv_parser.print_help()
        sys.exit()
        
    return args

def open_storage(filemode: str):
    filename = 'info.pass'
    file = open(filename, filemode)
    return file
    
def add_data():
    password_file = open_storage('a+')
    
    site = input("site: ")
    username = input("username: ")
    password = input("password: ")
    
    others = input("do you want to input other fields? (y/n) ")
    
    if others.lower() == "y":
        # TODO: add additional information to be inputted.
        pass
    
    dict_data = {
        'site' : site,
        'username' : username,
        'password' : password,
        'others' : {}
    }
    
    json_data = json.dumps(dict_data)
    password_file.write(json_data + "\n")
    password_file.close()
    
    
def main(args : argparse.Namespace):
    
    if args.cmd == "add":
        add_data()
    elif args.cmd == "view":
        print("view data")
    elif args.cmd == "rmv":
        print("remove data")

if __name__ == "__main__":
    args = tool_arguments()
    main(args)