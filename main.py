import argparse
import db_saver.db_saver as db_saver

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

    # Check if both a file and password are given
    if args.filename and args.password:
        db_saver.auto_backup(args.filename, args.password, args.email)
    elif args.filename and not args.password:
        print('Please specify a password')
    elif not args.filename and args.password:
        print('Please specify a file')
    # If there are no file or password, start the prompt
    else:
        db_saver.dialog()
