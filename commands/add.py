#!/usr/bin/env python3
#
# written by ZyzonixDev
# published by ZyzonixDevelopments
#
# Copyright (c) 2024 ZyzonixDevelopments
#
# date created  | 24-05-2024 09:48:06
# 
# file          | commands/add.py
# project       | ghsync
# file version  | 0.9.0
#

# add repository

# add takes following arguments: 
# required: 
# - repo-name as (-r [User/Repositoryname]) 
# - packages (-p [list-of-packages, separated by , wihtout space])
# optional: 
# - architectures (-a [list-of-archictectures, separated by , wihtout space]), if not provided all architectures will be synced

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
            argsComplete = scripts.utils.requiredArgsProvided({"-r": 1,"-p": 1}, splitArguments)
            if argsComplete:
                try: 
                    repo = splitArguments["-r"].split("/")[1]
                    status = True
                    repo_name = splitArguments["-r"]
                    packages = splitArguments["-p"]

                    wrongArchitectures = ""
                    if "-a" in splitArguments.keys(): 
                        architectures = splitArguments["-a"].lower()
                        archList = architectures.split(",")
                        for arch in archList:
                            if arch not in ["arm64", "amd64", "armhf"]: 
                                logging.writeError("Found invalid architecture: " + arch)
                                wrongArchitectures = True

                    else: architectures = "all"
                    if wrongArchitectures: 
                        logging.writeError("Failed to add repository: " + repo_name + ", found invalid architecture: " + str(architectures))
                        print("Failed to add architectures - invalid architecture found")
                        return False

                    insertData = [str(status), repo_name, packages, "", architectures, "", ""]

                    databaseConnection = sql.getDBConnection()

                    # check if repo already configured
                    sqlContent = ""
                    try:
                        sqlContent = sql.readData(databaseConnection, repo)
                    except:
                        logging.write("Cannot read data from SQL - normal when repository isn't configured.")
                        logging.writeExecError(traceback.format_exc())
                    if not sqlContent:
                        insertSuccessful = sql.insertData(databaseConnection, repo, insertData)
                        if insertSuccessful:
                            print("Added repository " + repo_name + " successfully.")
                            logging.write("Added repository " + repo_name + " successfully")
                            sql.closeDBConnection(databaseConnection)
                            return True
                    else:
                        print("Repository already configured. For changes reinstall it by removing and readding!")
                        logging.writeError("Repository " + repo_name + " already configured")
                except:
                    print("Failed to select required data from input!")
                    logging.writeError("Failed to select required data from input! Input was: " + str(args))
                    logging.writeExecError(traceback.format_exc())
                    

    def help(longHelp):
        output = ""
        if longHelp:
            output += "Help menu for 'add': Add a repository"
            output += "\n- required arguments are: -r [Repository], -p [Packages]"
            output += "\n- optional Arguments are: -a [Architectures] | valid architectures are: amd64, arm64, armhf"
            output += "\nRepository format: 'User/Repository', Packages format: package1,package2, Architecture format: arch1,arch2"
            output += "\nExample: ghsync add -r rustdesk/rustdesk -p rustdesk -a amd64,arm64"
            print(output)
            return True
        else:
            output += "[add] - add a repository"
            return output