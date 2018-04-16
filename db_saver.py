#!/usr/bin/env python3

import pymysql
import string
import csv
import datetime
import os
from pymysql import OperationalError
from pymysql import InternalError

#Class Connection
class Connection:
    #Class variables
    host = ""
    user = ""
    password = ""
    database = ""
    tables= ""
    connec = ""
    cursor = ""

    #Connect to the database on Initialization after assiging the class variables
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connec = pymysql.connect(self.host,self.user,self.password,self.database)
        self.cursor = self.connec.cursor()

    #Return all the available tables in the db
    def getTables(self):
        print('Retrieving tables')
        sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA=\'" + self.database + "\';"
        # Execute the SQL command
        self.cursor.execute(sql)
        # Fetch all the rows
        self.tables =self.cursor.fetchall()

    def getData(self, table):
        print('Retrieving data from table ' + table)
        sql = 'select * from ' + table + ';'
        self.cursor.execute(sql)

    def cleanTable(self, table):
        table = str(table)
        table = table[2:]
        table = table[:-3]
        return table

    def createFolder(self):
        print('Creating folder')
        now = datetime.datetime.now()
        directory = self.database + '-' + now.strftime("%Y-%m-%d")
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def exportData(self):
        for table in self.tables:
            directory = db.createFolder()
            table = db.cleanTable(table)
            now = datetime.datetime.now()
            filename = directory + '/' + table + '-' + now.strftime("%Y-%m-%d") + '.csv'
            with open(filename, "w", encoding="utf-8" ,newline='') as csv_file:  # Python 3 version
                self.getData(table)
                print('Writing data from table ' + table)
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in self.cursor.description]) # write headers
                csv_writer.writerows(self.cursor)


with open('databases.txt') as f:
    for line in f:
        if 'str' in line:
            break
        else:
            try:
                connectionInfo = line.split(',')
                print('Trying to connecto to database ' + connectionInfo[3][:-1])
                db = Connection(connectionInfo[0],connectionInfo[1],connectionInfo[2],connectionInfo[3][:-1])
            except OperationalError as error:
                code, message = error.args
                print('OperationalError', code, ':', message)
            except InternalError as error:
                code, message = error.args
                print('InternalError', code, ':', message)
            except:
                print('Unexpected error:'. sys.exc_info()[0])
                raise
            else:
                db.getTables()
                db.exportData()
                print('Database backup successfull')
