#!/usr/bin/env python3
import pymysql
import datetime
import csv
import os


# Class Database
from db_saver.db_saver_log import DbSaverLog


class Database:
    # Class variables
    host = ""
    user = ""
    password = ""
    database = ""
    tables = ""
    connec = ""
    cursor = ""

    # Connect to the database on Initialization after assiging the class variables
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connec = pymysql.connect(self.host, self.user, self.password, self.database)
        self.cursor = self.connec.cursor()

    # Return all the available tables in the db
    def get_tables(self):
        DbSaverLog.info("Retrieving tables")
        try:
            sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA=\'" + self.database + "\';"
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows
            self.tables = self.cursor.fetchall()
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise

    # Retrieve the data from a table
    def get_data(self, table):
        DbSaverLog.info("Retrieving data from table " + table)
        try:
            sql = "select * from " + table + ";"
            self.cursor.execute(sql)
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise

    # Return a clean table
    @staticmethod
    def clean_table(table):
        try:
            table = str(table)
            table = table[2:]
            table = table[:-3]
            return table
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise

    # Return the created directory
    def create_folder(self):
        try:
            DbSaverLog.info("Creating folder")
            now = datetime.datetime.now()
            file_dir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.join(file_dir,'../storage/backups/' + self.database + '-' + now.strftime('%Y-%m-%d-%H%M'))
            if not os.path.exists(directory):
                os.makedirs(directory)
            return directory
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise

    # Export data to a csv file
    def export_data(self):
        try:
            for table in self.tables:
                directory = self.create_folder()
                table = self.clean_table(table)
                now = datetime.datetime.now()
                filename = directory + '/' + table + '-' + now.strftime('%Y-%m-%d-%H%M') + '.csv'
                with open(filename, "w", encoding="utf-8", newline="") as csv_file:  # Python 3 version
                    self.get_data(table)
                    DbSaverLog.info('Writing data from table ' + table)
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([i[0] for i in self.cursor.description])  # write headers
                    csv_writer.writerows(self.cursor)
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise
