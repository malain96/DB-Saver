import pymysql
import datetime
import csv
import string
import os


# Class Connection
class Connection:
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
    def getTables(self):
        print("Retrieving tables")
        sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA=\'" + self.database + "\';"
        # Execute the SQL command
        self.cursor.execute(sql)
        # Fetch all the rows
        self.tables = self.cursor.fetchall()

    # Retrieve the data from a table
    def getData(self, table):
        print("Retrieving data from table ", table)
        sql = "select * from " + table + ";"
        self.cursor.execute(sql)

    # Return a clean table
    def cleanTable(self, table):
        table = str(table)
        table = table[2:]
        table = table[:-3]
        return table

    # Return the created directory
    def createFolder(self):
        print("Creating folder")
        now = datetime.datetime.now()
        directory = self.database + "-" + now.strftime("%Y-%m-%d")
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    # Export data to a csv file
    def exportData(self):
        for table in self.tables:
            directory = self.createFolder()
            table = self.cleanTable(table)
            now = datetime.datetime.now()
            filename = directory + "/" + table + "-" + now.strftime("%Y-%m-%d") + ".csv"
            with open(filename, "w", encoding="utf-8", newline="") as csv_file:  # Python 3 version
                self.getData(table)
                print('Writing data from table ' + table)
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in self.cursor.description])  # write headers
                csv_writer.writerows(self.cursor)
