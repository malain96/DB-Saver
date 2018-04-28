#!/usr/bin/env python3
import getpass
import os
from cipher import Cipher
from file_manager import File_manager

#Check which os is used and clear the terminal
def clearing():
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        clear = lambda: os.system('clear')
    elif _platform == "win64" or _platform == "win32":
        clear = lambda: os.system('cls')
    clear()


exit = False

#Enter ther file's password
password = getpass.getpass("Please enter your password: ")

#Init the file we are using
file = File_manager('databases.txt', password)

clearing()

#While we don't choose the action 99
while not exit:
    #Display all available actions
    print("\nActions:")
    print("0 - ADD DATABASE")
    print("1 - DELETE DATABASE")
    print("2 - CLEAR DATABASES")
    print("3 - SHOW DATABASES")
    print("4 - START BACKUP")
    print("98 - CLEAR")
    print("99 - EXIT")

    #Ask for the action we want to do
    action = input("Enter the action's number you want to use: ")

    clearing()

    #If we want to add a new db
    if action == "0":
        host = input("Enter the host: ")
        user = input("Enter the username: ")
        #Hidde the password
        dbPassword = getpass.getpass("Please enter your password:")
        database = input("Enter the database: ")
        #Add the new database to the file
        file.addDatabase(host,user,dbPassword,database)

    #If we want to delete a db
    elif action == "1":
        if file.isEmpty():
            print("You can't delete a database, your file is empty!")
        else:
            file.showDatabases()
            dbId = input("Enter the number of the database you want to delete: ")
            file.deleteDatabase(dbId)

    #if we want to clear the file
    elif action == "2":
        file.clearDatabases()

    #If we want to see the databases
    elif action == "3":
        #Show the databases
        if file.isEmpty():
            print("You can't display databases, your file is empty!")
        else:
            file.showDatabases()

    #If we want to start the back up
    elif action == "4":
        #Start the backup
        if file.isEmpty():
            print("You can't start the backup , your file is empty!")
        else:
            file.backupDatabases()

    #If we want to clear
    elif action == "98":
        #Clear
        clearing()

    #If we want to exit
    elif action == "99":
        #Exit the program
        exit = True
    else:
        print("Please enter a valid number")
