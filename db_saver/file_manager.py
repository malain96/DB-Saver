import os

from db_saver.cipher import Cipher
from pymysql import OperationalError
from pymysql import InternalError
from db_saver.database import Database


class FileManager:
    # Class variables
    file = ""
    key = ""

    # Init
    def __init__(self, file, key):
        self.file = file
        self.key = key

    # Add a database to the file
    def add_database(self, host, user, db_password, database):
        try:
            cipher = Cipher(self.key)
            text_file = open(self.file, "a")
            if os.path.getsize(self.file) > 0:
                text_file.write('\n')
            text_file.write(
                cipher.encode(host) + "," + cipher.encode(user) + "," + cipher.encode(db_password) + "," + cipher.encode(
                    database))
            text_file.close()
            print("Database Added!")
        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise

    # Show databases in the file
    def show_databases(self):
        print("Databases:")
        try:
            cipher = Cipher(self.key)
            count = 1
            with open(self.file) as f:
                for line in f:
                    if "str" in line:
                        break
                    else:
                        connection_info = line.split(",")
                        decoded_host = cipher.decode(connection_info[0])
                        decode_db = cipher.decode(connection_info[3])
                        print(str(count), "-", decoded_host + "/" + decode_db)
                        count += 1
        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise

    # Backup databases
    def backup_databases(self):
        try:
            cipher = Cipher(self.key)
            with open(self.file) as f:
                for line in f:
                    if "str" in line:
                        break
                    else:
                        connection_info = line.split(',')
                        print("Trying to connecto to database", cipher.decode(connection_info[3]))
                        db = Database(cipher.decode(connection_info[0]), cipher.decode(connection_info[1]),
                                      cipher.decode(connection_info[2]), cipher.decode(connection_info[3]))
                        db.get_tables()
                        db.export_data()
                        print("Database backup successful")
        except OperationalError as error:
            code, message = error.args
            print("OperationalError", code, ":", message)

        except InternalError as error:
            code, message = error.args
            print("InternalError", code, ":", message)

        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise

    # Clear databases file
    def clear_databases(self):
        try:
            f = open(self.file, "r+")
            f.truncate()
            print("Databases cleared!")
        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise

    # Delete a databse
    def delete_database(self, id):
        try:
            with open(self.file, "r") as f:
                lines = f.readlines()
                lines.pop(int(id) - 1)
                f.close()
            with open(self.file, "w") as f:
                f.writelines(lines)
                f.close()
                print("Database", id, "deleted!")
        except IndexError:
            print("The database you tried to remove doesn't exist!")
        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise

    def is_empty(self):
        try:
            if os.path.getsize(self.file) > 0:
                return False
            else:
                return True
        except OSError as error:
            code, message = error.args
            print("OSError", code, ":", message)
        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise
