# project
import helpers

# python
import os
import sqlite3
import inspect
import logging

import commonVariables

db_name = "sunnah.db"

class Database:
    def __init__(self, logger):
        self.logger = logger
    
    def create_database(self, conn):
        fn = helpers.get_function_name(inspect.currentframe())
        if os.path.isfile(db_name):
            self.logger.post_log("{}: database already exists".format(fn), logging.INFO)
            return
        
        conn.execute('''CREATE TABLE Hadiths
         (HADITH_KEY TEXT NOT NULL,
         HADITH_BLOB TEXT NOT NULL);''')
        self.logger.post_log("{}: database initialized".format(fn), logging.INFO)
    
    def get_connection(self):
        conn = sqlite3.connect(db_name)
        return conn
    
    def is_data_exist(self, conn, key):
        data = self.get_data(conn, key)
        if helpers.is_error(data):
            return False
        return True

    def get_data(self, conn, key):
        fn = helpers.get_function_name(inspect.currentframe())
        rows = conn.execute("SELECT HADITH_BLOB from Hadiths where HADITH_KEY = ?", (key,))
        data = None
        for row in rows:
            data = row[0]
        
        if data is None:
            data = self.logger.post_log("{}: {}: failed to get data with key: {}".format(commonVariables.errorPfx, fn, key), logging.ERROR)
        
        return data


        
    def insert_data(self, conn, key, blob):
        fn = helpers.get_function_name(inspect.currentframe())
        response = True
        if self.is_data_exist(conn, key):
            self.logger.post_log("{}: key already exists".format(fn), logging.INFO)
            return response


        try:
            conn.execute("INSERT INTO Hadiths (HADITH_KEY, HADITH_BLOB) VALUES (?, ?)", (key, blob,))
            conn.commit()
        except Exception as e:
            response = self.logger.post_log("{}: {}: error occured while inserting data with key: {}, error: {}".format(commonVariables.errorPfx, fn, key, e), logging.ERROR)
        
        return response

    
    def delete_data(self, conn, key):
        fn = helpers.get_function_name(inspect.currentframe())
        response = True
        if not self.is_data_exist(conn, key):
            self.logger.post_log("{}: key does not exist. nothing to delete".format(fn), logging.INFO)
            return response

        try:
            conn.execute("DELETE FROM Hadiths WHERE HADITH_KEY=?", (key,))
            conn.commit()
        except Exception as e:
            response = self.logger.post_log("{}: {}: error occured while inserting data with key: {}, error: {}".format(commonVariables.errorPfx, fn, key, e), logging.ERROR)
        
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