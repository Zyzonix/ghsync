#!/usr/bin/env python3
#
# written by ZyzonixDev
# published by ZyzonixDevelopments
#
# Copyright (c) 2024 ZyzonixDevelopments
#
# date created  | 24-05-2024 09:57:34
# 
# file          | scripts/logHandler.py
# project       | ghsync
# file version  | 1.0.0
#
import config

from datetime import datetime

# time for logging / console out
class ctime():
    def getTime():
        curTime = "" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        return curTime

# main log function
class logging():

    def toFile(msg):
        if config.LOGGING:
            try:
                logFile = open(config.LOGDIR + "ghsync.log", "a")
                logFile.write(msg + "\n")
                logFile.close()
            except:
                logging.writeError("Failed to open logfile directory, maybe a permission error?")

    def write(msg):
        message = str(ctime.getTime() + " INFO   | " + str(msg))
        logging.toFile(message)

    def writeError(msg):
        message = str(ctime.getTime() + " ERROR  | " + msg)
        logging.toFile(message)

    # log/print error stack trace
    def writeExecError(msg):
        message = str(msg)
        logging.toFile(message)

    def writeDebug(msg):
        # check if loglevel is debug (1=INFO,2=DEBUG)
        if config.LOGLEVEL == 2:
            message = str(ctime.getTime() + " DEBUG  | " + msg)
            logging.toFile(message)
    
    def writeSubprocessout(msg):
        for line in msg:
            line = str(line)
            line = line[:-3]
            line = line[3:]
            logging.write("SYS   | " + line)
    
