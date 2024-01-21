# project
import helpers
import timeFunctions

# python
import os
import sqlite3
import inspect
import logging

import commonVariables

db_name = "sunnah.db"
table_name = "Hadiths"

class DatabaseHadith:
    def __init__(self, logger):
        self.logger = logger
        self.get_connection()
    
    def get_connection(self):
        conn = sqlite3.connect(db_name)
        self.conn = conn
    
    def check_if_table_exists(self):
        fn = helpers.get_function_name(inspect.currentframe())
        rows = self.conn.execute("SELECT name FROM sqlite_master WHERE name = ?", (table_name,))
        data = None
        for row in rows:
            data = row[0]
        
        if data is None:
            self.logger.post_log("{}: {}: table does not exist".format(commonVariables.errorPfx, fn), logging.ERROR)
            return False
        
        return True

    def create_database(self):
        fn = helpers.get_function_name(inspect.currentframe())
        if self.check_if_table_exists():
            self.logger.post_log("{}: table already exists".format(fn), logging.INFO)
            return
        else:
            self.logger.post_log("{}: creating table".format(fn), logging.INFO)

        
        self.conn.execute('''CREATE TABLE Hadiths
         (HADITH_KEY TEXT NOT NULL UNIQUE,
         HADITH_BLOB TEXT NOT NULL);''')
        self.logger.post_log("{}: database initialized".format(fn), logging.INFO)
    
    def is_data_exist(self, key):
        data = self.get_data(key)
        if helpers.is_error(data):
            return False
        return True

    def get_data(self, key):
        fn = helpers.get_function_name(inspect.currentframe())
        rows = self.conn.execute("SELECT HADITH_BLOB from Hadiths where HADITH_KEY = ?", (key,))
        data = None
        for row in rows:
            data = row[0]
        
        if data is None:
            data = self.logger.post_log("{}: {}: failed to get data with key: {}".format(commonVariables.errorPfx, fn, key), logging.ERROR)
        
        return data
    
    def get_all_data(self):
        fn = helpers.get_function_name(inspect.currentframe())
        cur = self.conn.cursor()
        cur.execute("SELECT * from Hadiths")
        rows = cur.fetchall()
    
        keys = []
        values = []
        for row in rows:
            keys.append(row[0])
            values.append(row[1])

        return keys, values


        
    def insert_data(self, key, blob, grade):
        fn = helpers.get_function_name(inspect.currentframe())
        response = True
        if self.is_data_exist(key):
            self.logger.post_log("{}: key already exists".format(fn), logging.DEBUG)
            return response

        current_time = timeFunctions.get_current_time()

        try:
            self.conn.execute("INSERT INTO Hadiths (HADITH_KEY, HADITH_BLOB, LAST_UPDATED, Grade) VALUES (?, ?, ?, ?)", (key, blob, current_time, grade))
            self.conn.commit()
        except Exception as e:
            response = self.logger.post_log("{}: {}: error occured while inserting data with key: {}, error: {}".format(commonVariables.errorPfx, fn, key, e), logging.ERROR)
        
        return response

    
    def delete_data(self, key):
        fn = helpers.get_function_name(inspect.currentframe())
        response = True
        if not self.is_data_exist(key):
            self.logger.post_log("{}: key does not exist. nothing to delete".format(fn), logging.INFO)
            return response

        try:
            self.conn.execute("DELETE FROM Hadiths WHERE HADITH_KEY=?", (key,))
            self.conn.commit()
        except Exception as e:
            response = self.logger.post_log("{}: {}: error occured while inserting data with key: {}, error: {}".format(commonVariables.errorPfx, fn, key, e), logging.ERROR)
        
        return response

    def run_alter_query(self, query):
        fn = helpers.get_function_name(inspect.currentframe())
        response = True
        if "ALTER" not in query:
            response = self.logger.post_log("{}: query: {}, does not have the ALTER keyword".format(fn, query), logging.ERROR)
            return response
        
        try:
            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            response = self.logger.post_log("{}: {}: error occured while altering data, error: {}, query: {}".format(commonVariables.errorPfx, fn, e, query), logging.ERROR)
        
        return response
    
    def run_update_query(self, query):
        fn = helpers.get_function_name(inspect.currentframe())
        response = True
        if "UPDATE" not in query:
            response = self.logger.post_log("{}: query: {}, does not have the UPDATE keyword".format(fn, query), logging.ERROR)
            return response
        
        try:
            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            response = self.logger.post_log("{}: {}: error occured while updating data, error: {}, query: {}".format(commonVariables.errorPfx, fn, e, query), logging.ERROR)
        
        return response

    def test_func(self):
        conn = sqlite3.connect('test.db')

        print ("Opened database successfully")

        conn.execute('''CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);''')
        print("Table created successfully")


        conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (1, 'Paul', 32, 'California', 20000.00 )")

        conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")


        cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
        for row in cursor:
            print("ID = ")
            print(row[0])
            print("NAME = ")
            print(row[1])
            print("ADDRESS = ")
            print(row[2])
            print("SALARY = ")
            print(row[3])

        print("Operation done successfully")
        conn.close()