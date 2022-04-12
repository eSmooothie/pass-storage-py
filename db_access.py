import logging
import os
import sqlite3
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class InfoDataModel:
    def __init__(self, name, username, password, created_at, ref=None):
        self.name = name
        self.username = username
        self.password = password
        self.created_at = created_at
        self.others = {}
        if ref is None:
            self.ref = hash((name, username, password, created_at))
        else:
            self.ref = ref

    def add_other_field(self, field, value):
        self.others[field] = value
    
    def tuple_format(self) -> tuple:
        return (self.ref, self.name, self.username, self.password, self.created_at)

    def dict_format(self) -> dict:
        return {'ref': self.ref, 'name': self.name, 'username':self.username, 'password':self.password, 'created_at':self.created_at}

    def __str__(self):
        return f"InfoDataModel(ref={self.ref}, name={self.name}, username={self.username}, password={self.password}, created_at={self.created_at})"

class Database:

    def __init__(self):
        logging.debug("INIT DB")
        # check if db file exist
        db_exist = os.path.isfile(ROOT_DIR + '/password.db')
        self.__db_conn = sqlite3.connect(ROOT_DIR + '/password.db')
        self.__db_cursor = self.__db_conn.cursor()

        if not db_exist:
            
            logging.info("CREATING NECESSARY TABLES")
            self.__db_cursor.execute('''CREATE TABLE info (ref text, name text, username text, password text, created_at text)''') 
            self.__db_cursor.execute('''CREATE TABLE other_info (ref text, field text, value text)''')
            self.__db_conn.commit()

    @property
    def db_cursor(self):
        return self.__db_cursor

    def get_info(self, ref_no:str):
        res = self.__db_cursor.execute(f'''
            SELECT
                *
            FROM `info`
            WHERE `ref`={ref_no}
        ''')
        res = res.fetchall()

        if len(res) == 0:
            print(f"No information found in ref#{ref_no}.\nTry `mypass view` or `mypass view -h`")
            sys.exit(1)

        for row in res:
            ref, name, username, password, created_at = row
            info_data = InfoDataModel(
                ref=ref, 
                name=name,
                username=username,
                password=password,
                created_at=created_at
                )
            print(f"Reference {info_data.ref}")
            print(f"\tname: {info_data.name}")
            print(f"\tusername: {info_data.username}")
            print(f"\tpassword: {info_data.password}")
            print(f"\tcreated at: {info_data.created_at}")

        other = self.__db_cursor.execute(f'''
            SELECT
                *
            FROM `other_info`
            WHERE `ref`={ref_no}
        ''')
        print("Other fields:")
        o_fields = other.fetchall()
        logging.debug("Other field: {0} Len: {1}".format(o_fields, len(o_fields)))
        if len(o_fields) == 0:
            print("\tNone")
        else:
            for row in o_fields:
                ref, field, value = row
                print(f"\t{field}: {value}")
        other.close()

    def get_all_info(self, limit:int = 5, offset:int=0):
        res = self.__db_cursor.execute(f'''SELECT 
            `ref` AS `reference`,
            `name` AS `site`,
            `username` AS `username`,
            `password` AS `password`,
            `created_at` AS `created_at`
            FROM `info` LIMIT {limit} OFFSET {offset}
            ''')
        res = res.fetchall()

        if len(res) == 0:
            print("No data stored.\n\nTo add data `mypass add`.\n")
            sys.exit(0)
        
        print("Limit:{0} Offset:{1}\n".format(limit, offset))
        
        for row in res:
            ref, name, username, password, created_at = row
            info_data = InfoDataModel(
                ref=ref, 
                name=name,
                username=username,
                password=password,
                created_at=created_at
                )
            print(f"Reference {info_data.ref} ({info_data.created_at})")
            print(f"\tname: {info_data.name}")
            print(f"\tusername: {info_data.username}")
            print(f"\tpassword: {info_data.password}\n")
            
    def filter_info(self, **kwargs):
        logging.debug(f"at filter_info(). kwargs={kwargs}")
        
        expression = ""
        
        for field, value in kwargs.items():
            if value:
                expression += f"`{field}` LIKE '%{value}%' AND "

        expression += "1"
        
        logging.debug(f"at filter_info(). where_clause={expression}")
        
        filter_sql = f'''SELECT * FROM `info` WHERE {expression}'''
        
        logging.debug(f"at filter_info(). query={filter_sql}")
        
        res = self.__db_cursor.execute(filter_sql)
        res = res.fetchall()
        
        logging.debug(f"at filter_info(). result={res}")
        
        if len(res) == 0:
            print("No match found.")
            sys.exit(0)
        
        print("Found {0} data.\n".format(len(res)))
        
        for row in res:
            ref, name, username, password, created_at = row
            info_data = InfoDataModel(
                ref=ref, 
                name=name,
                username=username,
                password=password,
                created_at=created_at
                )
            print(f"Reference {info_data.ref} ({info_data.created_at})")
            print(f"\tname: {info_data.name}")
            print(f"\tusername: {info_data.username}")
            print(f"\tpassword: {info_data.password}\n")
    
    def remove_data(self, ref_no:str):
        del_sql = f'DELETE FROM `info` WHERE `ref` LIKE {ref_no}'
        logging.info(f'DELETING ref no:{ref_no}')
        self.__db_cursor.execute(del_sql)

        del_other_sql = f'DELETE FROM `other_info` WHERE `ref` LIKE {ref_no}'
        self.__db_cursor.execute(del_other_sql)
        
    def remove_all(self):
        del_sql = 'DELETE FROM `info`'
        logging.info('DELETING ALL DATA.')
        self.__db_cursor.execute(del_sql)
    
    def insert_info_data(self, data : InfoDataModel):
        insert_sql = 'INSERT INTO info VALUES (?, ?, ?, ?, ?)'
        self.__db_cursor.execute(insert_sql, data.tuple_format())
        logging.info(f"INSERTING {data}")

    def insert_other_info_data(self, data: tuple):
        insert_sql = 'INSERT INTO other_info VALUES (?, ?, ?)'
        self.__db_cursor.execute(insert_sql, data)
        logging.info(f"INSERTING {data}")

    def commit(self):
        self.__db_conn.commit()
        logging.info(f"COMMIT CHANGES TO DB.")

    def close(self):
        self.__db_conn.close()



