#!/usr/bin/env python3
import os
import subprocess
import gbconfig
import logging
from resources import testResult
from tests.unit_test import register_gen_test
from tools.log import logMsg

class ut_compare_output:
    def __init__(self, config):
        self.name = "ut_compare_output"
        self.maxPoints = 10
        self.config = config

    # Define your unit test here
    def run(self, submission):
        r = testResult.ut_result()
        logMsg(self.config, "Running unit test....")
        r.name = self.name
        r.maxPoints = self.maxPoints
        r.points = r.maxPoints
        r.passed = True

        # Set up our paths
        logMsg(self.config, "Making folders and setting paths")
        exePath = submission.workingPath + '/' <exeName>
        inputFolder = self.config.dir_tests+'/'+self.config.aid
        outputFolder = self.config.dir_output + '/' + self.config.aid + \
                           '/unit_test_output/'
        # Optional input file to feed to program through stdin
        inputFile = inputFolder+'/ut_input.txt'
        # Golden image of what is expected to be returned
        masterFile = inputFolder+'/ut_master.txt'
        # What file to write stdout to
        outputFile = outputFolder+'/'self.name+'_'+submission.student.sid+".txt"
        # Create any of the needed folders that don't exist
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)

        # Run the test and capture the output
        logMsg(self.config, "Running executable")
        inf = open(inputFile,'r')
        outf = open(outputFile,'w+') 
        output = subprocess.run([exePath],stdin=inf,encoding="utf-8",\
                stdout=outf, stderr=subprocess.PIPE)

        # Read the student output and master output to memory
        stdntOutput = ""
        outf.seek(0)
        for line in outf:
            stdntOutput += line.lower()
        mstrOutput = ""
        with open(masterFile,'r') as f:
            for line in f:
                mstrOutput += line.lower()

        # Start comparing the outputs line by line
        logMsg(self.config, "Comparing output")
        stdntLines = stdntOutput.split('\n')
        mstrLines = mstrOutput.split('\n')
        lCount = len(stdntLines)
    
        if lCount != len(mstrLines):
            r.passed = False
            r.comments += "Line count from student output did not match "+\
                            "line count from master output file. Needs "+\
                            "manual review\n"
            # If the master has fewer lines, use that count to avoid exceptions
            if lCount > len(mstrLines):
                lCount = len(mstrLines)
                        
        for i in range(0,lCount):
            # Strip all whitespace from the lines and compare
            print(mstrLines[i])
            if "".join(stdntLines[i].split()) != "".join(mstrLines[i].split()):
                r.passed = False
                r.points -= 1 
                r.comments += "Output line mismatch\n\tExpected line: {0}\n\tReceived line: {1}\n".format(\
                                       mstrLines[i], stdntLines[i])

        if r.passed:
            logMsg(self.config, "Test succeeded!")
            r.comments += "Succesfully passed the expression evaluation test!\n"

        return r 

if __name__ == "__main__":
    print("hello")

# Register this unit test with gradebot
register_gen_test("ut_compare_output",ut_compare_output)
