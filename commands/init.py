#!/usr/bin/env python3
#
# written by ZyzonixDev
# published by ZyzonixDevelopments
#
# Copyright (c) 2024 ZyzonixDevelopments
#
# date created  | 24-05-2024 12:09:42
# 
# file          | commands/init.py
# project       | ghsync
# file version  | 0.9.0
#

# init sqlite db

from scripts.logHandler import logging
from scripts.sqlHandler import sql
import config

import traceback

class command():
    
    def execute(args):
        logging.write("Initializing ghsync database: " + config.SQLITEDB)
        try:
            dbConnection = sql.getDBConnection()
            sql.databaseSetup(dbConnection)
            sql.closeDBConnection(dbConnection)
            print("Initialized database")
            return True
        except:
            logging.writeError("Failed to initialize database")
            logging.writeExecError(traceback.format_exc())
            return False
        
    def help():
        return "Takes no arguments, just initializes the database (sqlite3)"