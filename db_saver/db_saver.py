#!/usr/bin/env python3
import getpass
import logging
import os

from db_saver.db_saver_log import DbSaverLog
from db_saver.file_manager import FileManager
from db_saver.email import Email


# Check which os is used and clear the terminal
def clearing():
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        clear = lambda: os.system('clear')
    elif _platform == "win64" or _platform == "win32":
        clear = lambda: os.system('cls')
    clear()


def dialog():
    logging.info('Entering prompt')
    exit_dialog = False

    # Enter the database's file - If the file doesn't exist, it will be created
    file_to_open = input(
        "Please enter the file containing the databases [leave empty to use the default 'databases.txt']:")

    # Check if we should use the default file
    if len(file_to_open.strip()) == 0:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_to_open = os.path.join(file_dir, '../storage/databases.txt')

    # Enter the file's password
    password = getpass.getpass("Please enter the password to read this file: ")
    # Prevent the user from submitting an empty password
    while not password:
        DbSaverLog.info("Please, provide a password!")
        password = getpass.getpass("Please enter the password to read this file: ")

    # Init the file we are using
    file = FileManager(file_to_open, password)

    clearing()

    # While we don't choose the action 99
    while not exit_dialog:
        # Display all available actions
        print("\nActions:")
        print("0 - ADD DATABASE")
        print("1 - DELETE DATABASE")
        print("2 - CLEAR DATABASES")
        print("3 - SHOW DATABASES")
        print("4 - START BACKUP")
        print("98 - CLEAR")
        print("99 - EXIT")

        # Ask for the action we want to do
        action = input("Enter the action's number you want to use: ")

        clearing()

        # If we want to add a new db
        if action == "0":
            logging.info('Entering database creation')
            host = input("Enter the host: ")
            user = input("Enter the username: ")
            # Hide the password
            db_password = getpass.getpass("Please enter your password:")
            database = input("Enter the database: ")
            # Add the new database to the file
            file.add_database(host, user, db_password, database)

        # If we want to delete a db
        elif action == "1":
            if file.is_empty():
                DbSaverLog.info("You can't delete a database, your file is empty!")
            else:
                logging.info('Entering database deletion')
                file.show_databases()
                db_id = input("Enter the number of the database you want to delete: ")
                file.delete_database(db_id)

        # if we want to clear the file
        elif action == "2":
            logging.info('Entering database clearing')
            file.clear_databases()

        # If we want to see the databases
        elif action == "3":
            # Show the databases
            if file.is_empty():
                DbSaverLog.info("You can't display databases, your file is empty!")
            else:
                logging.info('Entering database display')
                file.show_databases()

        # If we want to start the back up
        elif action == "4":
            # Start the backup
            if file.is_empty():
                DbSaverLog.info("You can't start the backup , your file is empty!")
            else:
                logging.info('Entering database backup')
                file.backup_databases()

        # If we want to clear
        elif action == "98":
            # Clear
            logging.info('Entering prompt clearing')
            clearing()

        # If we want to exit
        elif action == "99":
            logging.info('Exiting the prompt')
            # Exit the program
            exit_dialog = True
        else:
            DbSaverLog.info("Please enter a valid number")


# Function used to start a backup with a command line
def auto_backup(file_to_open, password, email):
    try:
        logging.info('Entering command line backup')
        # Retrieve the database
        file = FileManager(file_to_open, password)
        # Start the backup
        file.backup_databases()
        # If an email is set, send a confirmation email
        if email:
            logging.info('Entering command line backup email confirmation')
            message = Email.success_message(email)
            Email.send(email, message)
    except Exception as error:
        # If an email is set, send an error email
        if email:
            logging.info('Entering command line backup error email')
            message = Email.error_message(email, str(error))
            Email.send(email, message)
