#!/usr/bin/env python3
import os
import shutil
from tools.log import logMsg
from gbconfig import gbconfig

def createAssignment(config, aid):
    dir_list = [config.dir_submissions, config.dir_output, config.dir_tests]
    for d in dir_list:
        folder = d + '/' + aid
        logMsg(config, "Making folder at {0}".format(folder))
        if not os.path.isdir(folder):
            os.makedirs(folder)
        # the test folder requires a few extra steps
        if d == config.dir_tests:
            ut_files = os.listdir(d+'/template')
            for file_name in ut_files:
                full_file_name = os.path.join(d+'/template', file_name)
                if (os.path.isfile(full_file_name)):
                    shutil.copy(full_file_name, folder)

def removeAssignment(config, aid, r_ut):
    dir_list = [config.dir_submissions, config.dir_output, config.dir_tests]
    for d in dir_list:
        if d == config.dir_tests and r_ut[0] != 'y':
            continue
        folder = d + '/' + aid
        logMsg(config, "Removing folder at {0}".format(folder))
        if os.path.isdir(folder):
            shutil.rmtree(folder)

if __name__ == "__main__":
    print("hello!")
