#!/usr/bin/env python3
#
# written by ZyzonixDev
# published by ZyzonixDevelopments
#
# Copyright (c) 2024 ZyzonixDevelopments
#
# date created  | 23-05-2024 08:40:39
# 
# file          | ghsync.py
# project       | ghsync
# file version  | 0.9.0
#
import commands.add
import commands.disable
import commands.enable
import commands.help
import commands.remove
import commands.show
import commands.sync
from scripts.logHandler import logging

from datetime import datetime
import sys

# time for logging / console out
class ctime():
    def getTime():
        curTime = "" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        return curTime

# collect and build command list
def commandBuilder():
    command = {}
    mainDef = "command"
    try: 
        command["add"] = getattr(commands.add, mainDef)
        command["disable"] = getattr(commands.disable, mainDef)
        command["enable"] = getattr(commands.enable, mainDef)
        command["help"] = getattr(commands.help, mainDef)
        command["remove"] = getattr(commands.remove, mainDef)
        command["show"] = getattr(commands.show, mainDef)
        command["sync"] = getattr(commands.sync, mainDef)
    except:
        return False
    return command


# handle input
def splitArguments():
    allArgs = sys.argv
    if len(allArgs) > 1:
        command = allArgs[1] 
        allArgs.pop(0)
        allArgs.remove(command)
        args = allArgs
        return command, args
    else:
        return "help", []

class init():
    def __init__(self):
        commands = commandBuilder()
        if not commands: 
            logging.writeError("Failed to import commands")
            return
        command, args = splitArguments()
        if command in commands:
            commands[command].execute(args)
        else:
            print("Failed! Command not found - Type 'help' for help menu.")
            logging.writeError("Command not found")
            logging.writeDebug("Command provided: " + command)

if __name__ == "__main__":
    init() 