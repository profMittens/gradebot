#!/usr/bin/env python3
import subprocess
import gbconfig
import logging
from resources import testResult
from tests.unit_test import register_gen_test
from tools.log import logMsg

class ut_compile:
    def __init__(self, config):
        self.name = "ut_compile"
        self.maxPoints = 10
        self.config = config

    # Define your unit test here
    def run(self, submission):
        r = testResult.ut_result()
        logMsg(self.config, "Running unit test 1")
        r.name = self.name
        r.maxPoints = self.maxPoints
        logMsg(self.config, "Calling make")
        output = subprocess.run(['make', '-C', submission.workingPath],\
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if output.returncode != 0:
            logMsg(self.config, "Make failed with: "+output.stderr.decode("utf-8"))
            r.passed = False
            r.points = 0
            r.comments = "Call to make failed, make output:\n " +\
                          output.stderr.decode("utf-8")+'\n'
        else:
            logMsg(self.config, "Make was successful!")
            r.passed = True
            r.points = self.maxPoints
            r.comments = "Successfully compiled!"

        return r 

if __name__ == "__main__":
    print("hello")

# Register this unit test with gradebot
register_gen_test("ut_compile",ut1)
