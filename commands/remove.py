#!/usr/bin/env python3
#
# written by ZyzonixDev
# published by ZyzonixDevelopments
#
# Copyright (c) 2024 ZyzonixDevelopments
#
# date created  | 24-05-2024 09:48:24
# 
# file          | commands/remove.py
# project       | ghsync
# file version  | 0.9.0
#

# remove repository

# remove takes following arguments: 
# required: 
# - repo-name as (-r [User/Repositoryname]) 

import scripts.utils 
from scripts.logHandler import logging
from scripts.sqlHandler import sql

import traceback

class command():

    def execute(args):
        argsClean = scripts.utils.verifyArgs(args)
        if argsClean:
            splitArguments = scripts.utils.formatArgs(args)
            # check if required arguments are provided
            argsComplete = scripts.utils.requiredArgsProvided({"-r": 1}, splitArguments)
            if argsComplete:
                repo = splitArguments["-r"].split("/")[1]
                repo_name = splitArguments["-r"]

                databaseConnection = sql.getDBConnection()

                # check if repo is configured
                sqlContent = ""
                try:
                    sqlContent = sql.readData(databaseConnection, repo)
                except:
                    logging.write("Cannot read data from SQL - normal when repository isn't configured.")
                    logging.writeExecError(traceback.format_exc())
                if sqlContent:
                    confirm = input("Are you sure? [y/n]: ")
                    if confirm == "y":
                        removeSuccessful = sql.removeData(databaseConnection, repo)
                        if removeSuccessful:
                            print("Removed repository " + repo_name + " successfully.")
                            logging.write("Removed repository " + repo_name + " successfully")
                            sql.closeDBConnection(databaseConnection)
                            return True
                    else:
                        logging.writeError("Aborted or invalid answer: " + confirm)
                        print("Removal aborted!")
                        return False
                else:
                    print("Repository not configured.")
                    logging.writeError("Repository " + repo_name + " not configured")

    def help(longHelp):
        output = ""
        if longHelp:
            output += "Help menu for 'remove': Remove a repository"
            output += "\n- required arguments are: -r [Repository]"
            output += "\nRepository format: 'User/Repository'"
            output += "\nExample: ghsync add -r rustdesk/rustdesk"
            print(output)
            return True
        else:
            output += "[remove] - remove a repository"
            return output