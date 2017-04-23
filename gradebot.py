#!/usr/bin/env python3
import argparse
import logging
import sys
import os
import shutil

# add our packages to the python path
import tests
from tools.log import logMsg
from gbconfig import dataProvider
from gbconfig import gbconfig
from resources.submission import submissionHelper
from resources.student import studentHelper
from resources.testResult import ut_result

def getUnitTests(config):
    __import__("tests."+config.aid,fromlist=['*'])    
    return tests.unit_test.registered_tests

'''
    Run each unit test on an individual submission. The run function takes the
    submission as an argument and places information on the results of the unit
    test into the submission entry
'''
def runTests(submissions, unitTests, config):
    for sid, submission in submissions.items():
        for name, test in unitTests.items():
            testObj = unitTests[name](config)
            submission.results.append(testObj.run(submission))
        for r in submission.results:
            submission.maxPoints = submission.maxPoints + r.maxPoints
            submission.totalPoints = submission.totalPoints + r.points

        #save off the results to a file
        outDir = config.dir_output+'/'+config.aid
        submission.save(outDir)

def printResults(submissions, config):
    for sid, sub in submissions.items():
        logMsg(config, "Results for {0} - {1}".format(sid, sub.student.fName + " " + sub.student.lName))
        logMsg(config,"Total score: {0} of {1} possible".format(sub.totalPoints, sub.maxPoints))
        logMsg(config,"Individual test results")
        for r in sub.results:
            msg = "\tTest: {0}\n\tPassed: {1}\n\tPoints: {2} of {3}\n\tComments: {4}\n"\
                   .format(r.name, str(r.passed), r.points, r.maxPoints, r.comments)
            logMsg(config,msg)


'''
    Entry point to processing submissions downloaded from D2L. The assignment 
    submissions will need to be in the submissions directory already. This 
    function will then be able to parse the crazy naming scheme d2l uses to 
    name files, determine the latest submission, and then run unit tests on 
    each of the submissions.
'''
def d2lEp(config):
    d2ltools = d2lHelper(config)
    if not d2ltools.assignmentsExist():
        quit()
   
    logMsg(config,"Getting list of submissions")
    submissions = d2ltools.getSubmissions()

    logMsg(config,"Unzipping all submissions")
    d2ltools.unzip(submissions)
 
    logMsg(config,"Getting unit tests for assignment")
    unitTests = getUnitTests(config)

    logMsg(config,"Preparing to run tests on submissions")
    runTests(submissions, unitTests, config)

    printResults(submissions, config)

    logMsg(config,"Cleaning up working folder")
    shutil.rmtree(config.workingFolder)


def configureLogging(config):
    logPath = config.dir_output+"/gradebot.log"
    logging.basicConfig(filename=logPath, level=logging.DEBUG, \
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

if __name__ == "__main__":

    # Set up argument parsing, we require the dataprovider argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-dp","--dataprovider", help="where your assignments are \
            comming from. Options are: d2l, bb, gh, gl")
    parser.add_argument("-a","--aid", help="id of the assignment to be graded")
    parser.add_argument("-d","--debug", help="turn on debug prints")
    parser.add_argument("-c","--create", help="create a new assignment, this will create"\
            "all the folders in the right places")
    parser.add_argument('-r','--remove', help="removes assignment from gradebot")
    args = parser.parse_args()
   
    # Save the assignment id that is to be graded
    if args.aid:
        config = gbconfig(args.aid)
    else:
        config = gbconfig()

    # set up logging
    configureLogging(config)
    logMsg(config,"***********************************************************")
    logMsg(config,"-- GRADEBOT STARTING --")

    # Make sure the correct flags are used together
    if (args.dataprovider and not args.aid)\
        or (args.aid and not args.dataprovider):
        print("Data provider and assignment are both required together")
        quit()
    
    # Parse the data provider and set the correction option in the config
    if args.dataprovider == "d2l":
        logMsg(config, "Selected D2l as the data provider")
        config.dataProvider = dataProvider.D2L
    elif args.dataprovider == "bb":
        logMsg(config, "Selected BitBucket as the data provider")
        config.dataProvider = dataProvider.BITBUCKET
    elif args.dataprovider == "gh":
        logMsg(config, "Selected GitHub as the data provider")
        config.dataProvider = dataProvider.GITHUB
    elif args.dataprovider == "gl":
        logMsg(config, "Selected GitLab as the data provider")
        config.dataProvider = dataProvider.GITLAB
    
    if args.create:
        from tools.housekeeping import createAssignment
        print("Creating folders for " + args.create)
        createAssignment(config, args.create)
        print("Done")
        quit()
    elif args.remove:
        from tools.housekeeping import removeAssignment
        print("Also delete unit tests? [y/n]")
        r_ut = input()
        print("Removing " + args.remove)
        removeAssignment(config, args.remove, r_ut)
        print("Done")
        quit()
   


    outDir = config.dir_output+'/'+config.aid
    logMsg(config, "Creating output foder at {0}".format(outDir))
    if not os.path.isdir(outDir):
        os.makedirs(outDir)

    # Call the entry point for the data provider
    if config.dataProvider == dataProvider.D2L:
        from tools.d2l import d2lHelper
        logMsg(config, "Calling D2l entry point")
        d2lEp(config)
    else:
        print("Data provider not currently supported")
        logging.info("Data provider not currently supported")



