#!/usr/bin/env python3
import logging


class DbSaverLog:

    # Function used to log and print infos
    @staticmethod
    def info(message):
        print(message)
        logging.info(message)

    # Function used to log and print errors with a type
    @staticmethod
    def typed_error(err_type, code, message):
        err = err_type + " error " + str(code) + " : " + message
        print(err)
        logging.error(err)

