#!/usr/bin/env python3
import argparse
import logging
import os

import db_saver.db_saver as db_saver
from db_saver.db_saver_log import DbSaverLog

if __name__ == '__main__':
    # Parse the arguments if needed
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='filename', nargs='?',
                        help='File were your databases are located', metavar='FILE')
    parser.add_argument('-p', '--password', dest='password', nargs='?',
                        help='The database\'s password', metavar='PASSWORD')
    parser.add_argument('-e', '--email', dest='email', nargs='?',
                        help='Email to which you want to send a report', metavar='EMAIL')
    args = parser.parse_args()

    # Logging config
    file_dir = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(filename=os.path.join(file_dir, './storage/logs.txt'),
                        filemode='a',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    # Check if both a file and password are given
    if args.filename and args.password:
        db_saver.auto_backup(args.filename, args.password, args.email)
    elif args.filename and not args.password:
        DbSaverLog.info('Please specify a password')
    elif not args.filename and args.password:
        DbSaverLog.info('Please specify a file')
    # If there are no file or password, start the prompt
    else:
        db_saver.dialog()
