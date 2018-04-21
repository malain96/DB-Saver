import os
from cipher import Cipher
from pymysql import OperationalError
from pymysql import InternalError
from connection import Connection

class File_manager:

    #Class variables
    file = ""
    key = ""

    #Init
    def __init__(self, file, key):
        self.file = file
        self.key = key

    #Add a database to the file
    def addDatabase(self,host,user,dbPassword,database):
        cipher = Cipher(self.key)
        text_file = open(self.file, 'a')
        if(os.path.getsize(self.file) > 0):
            text_file.write('\n')
        text_file.write(cipher.encode(host) + ',' + cipher.encode(user) + ',' + cipher.encode(dbPassword) + ',' + cipher.encode(database))
        text_file.close()

    #Show databases in the file
    def showDatabases(self):
        cipher = Cipher(self.key)
        count = 1
        with open(self.file) as f:
            for line in f:
                if 'str' in line:
                    break
                else:
                    connectionInfo = line.split(',')
                    decodedHost = cipher.decode(connectionInfo[0])
                    decodeDb = cipher.decode(connectionInfo[3])
                    print(str(count) + ' - ' + decodedHost+'/'+decodeDb)
                    count+=1

    #Backup databases
    def backupDatabases(self):
        cipher = Cipher(self.key)
        with open(self.file) as f:
            for line in f:
                if 'str' in line:
                    break
                else:
                    try:
                        connectionInfo = line.split(',')
                        print('Trying to connecto to database ' + connectionInfo[3])
                        db = Connection(cipher.decode(connectionInfo[0]),cipher.decode(connectionInfo[1]),cipher.decode(connectionInfo[2]),cipher.decode(connectionInfo[3]))
                    except OperationalError as error:
                        code, message = error.args
                        print('OperationalError', code, ':', message)
                    except InternalError as error:
                        code, message = error.args
                        print('InternalError', code, ':', message)
                    except:
                        print('Unexpected error')
                        raise
                    else:
                        db.getTables()
                        db.exportData()
                        print('Database backup successfull')

    #Clear databases file
    def clearDatabases(self):
        f = open(self.file, 'r+')
        f.truncate()


    def deleteDatabase(self, id):
        with open(self.file, 'r') as f:
            lines = f.readlines()
            lines.pop(1)
            f.close()

        with open(self.file, 'w') as f:
            f.writelines(lines)
            f.close()
