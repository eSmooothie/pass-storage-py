import logging
import os
import sqlite3

class InfoDataModel:
    def __init__(self, site, username, password, created_at):
        self.site = site
        self.username = username
        self.password = password
        self.created_at = created_at
        self.others = {}
        self.ref = hash(site + username + password + created_at)

    def add_other_fields(self, data: dict):
        pass
    
    def tuple_format(self) -> tuple:
        return (self.ref, self.site, self.username, self.password, self.created_at)

    def dict_format(self) -> dict:
        return {'ref': self.ref, 'site': self.site, 'username':self.username, 'password':self.password, 'created_at':self.created_at}

    def __str__(self):
        return f"InfoDataModel(ref={self.ref}, site={self.site}, username={self.username}, password={self.password}, created_at={self.created_at})"

class Database:

    def __init__(self):
        logging.info("INIT DB")
        # check if db file exist
        db_exist = os.path.isfile('storepass.db')
        self.__db_conn = sqlite3.connect('storepass.db')
        self.__db_cursor = self.__db_conn.cursor()

        if not db_exist:
            logging.info("CREATING NECESSARY TABLES")
            self.__db_cursor.execute('''CREATE TABLE info (ref text, site text, username text, password text, created_at text)''') 
            self.__db_cursor.execute('''CREATE TABLE other_info (ref text, field text, value text)''')
            self.__db_conn.commit()

    @property
    def db_cursor(self):
        return self.__db_cursor

    def get_all_info(self, limit:int = 5):
        res = self.__db_cursor.execute(f'''SELECT 
            `ref` AS `reference`,
            `site` AS `site`,
            `username` AS `username`,
            `password` AS `password`,
            `created_at` AS `created_at`
            FROM `info` LIMIT {limit}
            ''')

        print(res.fetchall())

    def insert_data(self, data : InfoDataModel):
        insert_sql = 'INSERT INTO info VALUES (?, ?, ?, ?, ?)'
        self.__db_cursor.execute(insert_sql, data.tuple_format())
        self.__db_conn.commit()
        logging.info(f"INSERT {data}")

    def close(self):
        self.__db_conn.close()



