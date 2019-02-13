#!/usr/bin/env python3
import os

from db_saver.cipher import Cipher
from pymysql import OperationalError
from pymysql import InternalError
from db_saver.database import Database
from db_saver.db_saver_log import DbSaverLog


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
            DbSaverLog.info("Database Added!")
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
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
                        print(str(count) + "-" + decoded_host + "/" + decode_db)
                        count += 1
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
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
                        DbSaverLog.info("Trying to connect to database " + cipher.decode(connection_info[3]))
                        db = Database(cipher.decode(connection_info[0]), cipher.decode(connection_info[1]),
                                      cipher.decode(connection_info[2]), cipher.decode(connection_info[3]))
                        db.get_tables()
                        db.export_data()
                        DbSaverLog.info("Database backup successful")
        except OperationalError as error:
            code, message = error.args
            DbSaverLog.typed_error('OperationalError', code, message)

        except InternalError as error:
            code, message = error.args
            DbSaverLog.typed_error('InternalError', code, message)

        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise

    # Clear databases file
    def clear_databases(self):
        try:
            f = open(self.file, "r+")
            f.truncate()
            DbSaverLog.info("Databases cleared!")
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
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
                DbSaverLog.info("Database " + id + " deleted!")
        except IndexError:
            DbSaverLog.info("The database you tried to remove doesn't exist!")
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise

    def is_empty(self):
        try:
            if os.path.getsize(self.file) > 0:
                return False
            else:
                return True
        except OSError as error:
            code, message = error.args
            DbSaverLog.typed_error('OSError', code, message)
        except BaseException as error:
            code, message = error.args
            DbSaverLog.typed_error('Unexpected', code, message)
            raise
