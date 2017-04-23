#!/usr/bin/env python3
from enum import Enum
import os
import configparser

CONFIG_FILE = "config.ini"

# Enum for the various data providers gradebot could pull assignments from
class dataProvider(Enum):
    NA = 0
    D2L = 1
    BITBUCKET = 2
    GITLAB = 3
    GITHUB = 4

class gbconfig:
    def __init__(self, aid='a1'):
        # Parse our config file
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        # Set defaults
        self.dataProvider = dataProvider.NA
        self.aid = aid
        self.cwd = os.getcwd()
        self.cwd = self.cwd + '/'
        self.dir_submissions = self.cwd+config['default_settings']['dir_submissions']
        self.dir_input = self.cwd+config['default_settings']['dir_input']
        self.dir_tests = self.cwd+config['default_settings']['dir_tests']
        self.dir_output = self.cwd+config['default_settings']['dir_output']
        self.dir_assignments = self.dir_submissions + "/" + self.aid
        self.dir_class = self.dir_tests+"/"+config['default_settings']['class']
        self.max_points = 0 
        self.blacklist = config['default_settings']['blacklist'].split(',')
        self.dir_testsToRun = self.dir_tests+'/'+self.aid
        self.buildDir = self.cwd+'/'+config['default_settings']['build_dir']
        self.workingFolder = self.dir_assignments+'/tmp'
        self.debug = True
        self.gradeFile = config['default_settings']['grade_file']
        self.generateFeedback = False
        self.noGrade = False

if __name__ == "__main__":
    print("Running self test...")
    config = gbconfig()
    attrs = vars(config)
    print('\n'.join("%s: %s" % item for item in attrs.items()))
    print("Done")
