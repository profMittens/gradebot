#!/usr/bin/env python3
import os
import logging
import zipfile
import json
import csv
from tools.log import logMsg
from resources.student import studentHelper
from resources.submission import submissionHelper
from gbconfig import gbconfig
from datetime import datetime

'''
    Fix up D2L's weird timestamps to include 0 padded day and time info
'''
def fixUpDate(date):
    parts = date.split(' ')
    if(len(parts[2]) < 2):
        parts[2] = '0'+parts[2]
    if(len(parts[4]) < 4):
        parts[4] = '0'+parts[4]
    return str.join(' ',parts)

class d2lHelper:
    def __init__(self, config):
        self.config = config

    def unzip(self, submissions):
        if not os.path.isdir(self.config.workingFolder):
            os.makedirs(self.config.workingFolder)

        for sid,sub in submissions.items():
            try:
                zf = zipfile.ZipFile(sub.path)
                zi = zf.infolist()

                # make unique outer folder
                unzippedFolder = self.config.workingFolder+'/'+sid
                if not os.path.isdir(unzippedFolder):
                    os.makedirs(unzippedFolder)
                zf.extractall(unzippedFolder)
                
                # check to see if the student zipped a directory with code or 
                # just zipped the files together
                if zi[0].is_dir():
                    sub.workingPath = unzippedFolder+'/'+zi[0].filename
                else:
                    sub.workingPath = unzippedFolder
            except zipfile.BadZipfile:
                logMsg(self.config,"ERROR: bad zip file  {0}".format(submissions[sid].path))
            except zipfile.LargeZipFile:
                logMsg(self.config,"ERROR: need zip64  {0}".format(submissions[sid].path))

    def assignmentsExist(self):
        # Check if the submissions are in the submissions director
        if not os.path.exists(self.config.dir_assignments):
            logMsg(self.config,"ERROR: {0} does not exists, can't grade whats not there :(".\
                    format(self.config.dir_assignments))
            return False 
        # Check if there are folders in the directory
        if len([f for f in os.listdir(self.config.dir_assignments)\
                if os.path.isfile(os.path.join(self.config.dir_assignments, f))]) < 1:
            logMsg(self.config, "ERROR: {0} is empty, can't grade whats not there :(".\
                    format(self.config.dir_assignments))
            return False
        return True

    def getSubmissions(self):
        submissions = dict()
        files = os.listdir(self.config.dir_assignments)
        for f in files:
            if f in self.config.blacklist:
                logMsg(self.config,"Ignoring {0}, is in blacklist".format(f))
                continue

            #TODO parse out the student comments for the selected file
            if f == "index.html":
                continue

            si = f.split('-')
            print(si)
            student = studentHelper(si[0]+si[1], si[2].strip().split(' ')[0], si[2].strip().split(' ')[1])
            date = fixUpDate(si[3]).strip()

            # Check if the student submitted multiple files, take the one with
            # the newest date 
            if student.sid in submissions:
                oldEntry = datetime.strptime(submissions[student.sid].date, '%b %d, %Y %I%M %p') 
                newEntry = datetime.strptime(date, '%b %d, %Y %I%M %p') 
                if oldEntry > newEntry:
                    continue
            
            #TODO parse d2l html file for student comments and add them here
            submission = submissionHelper(student, date, self.config.dir_assignments+'/'+f, "", "", self.config.max_points, 0)
            submissions[student.sid] = submission

        return submissions

    def generateGrades(self):
        # read the gradebook into memory
        gradebook = []
        with open(self.config.gradeFile) as csvfile:
            reader = csv.reader(csvfile)
            for l in reader:
                gradebook.append(l)
        eolHdr = "End-of-Line Indicator"
        eol = "#"

        # load all of the submissions so we can insert the new grade into teh book
        gradesDir = self.config.dir_output + '/' + self.config.aid
        for f in os.listdir(gradesDir):
            if f[-4:] == "json":
                path = gradesDir+'/'+f
                with open(path) as jsonData:
                    sub = json.load(jsonData)
                
                gradebookHdr = self.config.aid + ' Points Grade <Numeric MaxPoints:{0}>'\
                    .format(sub['maxPoints'])
                for l in gradebook: 
                    if l[1] == sub['student']['lName'] and l[2] == sub['student']['fName']:
                        l[len(l)-1] = sub['totalPoints']
                        l.append(eol)
                        break
                    
         
        gradebook[0][len(gradebook[0])-1] = gradebookHdr
        gradebook[0].append(eolHdr)
       
        # insert 0's for anyone that didn't submit
        count = len(gradebook[0])
        for l in gradebook:
            if len(l) < count:
                l[len(l)-1] = ''
                l.append(eol)

        writer = csv.writer(open(self.config.gradeFile, 'w'))
        writer.writerows(gradebook)
        print("Gradebook updated, upload to d2l to add new grades") 

    def generateFeedback(self):
        # make feedback folder
        feedbackDir = self.config.dir_output + '/' + self.config.aid + '/feedback/'
        if not os.path.isdir(feedbackDir):
            os.makedirs(feedbackDir)
        gradesDir = self.config.dir_output + '/' + self.config.aid

        for f in os.listdir(gradesDir):
            if f[-4:] == "json":
                path = gradesDir+'/'+f
                with open(path) as jsonData:
                    sub = json.load(jsonData)
               
                feedbackFilePath = feedbackDir+f[:6]+'-'+f[6:12]+'.txt'
                feedback = open(feedbackFilePath,'w')
                feedback.write("Student: {0}".format(sub["student"]['fName']\
                            +' '+sub["student"]['lName']+'\n\n'))
                feedback.write("Overall Comments: {0}\n\n".format(sub["instructorComments"]))
                feedback.write("Per test comments\n")
                for r in sub["results"]:
                    feedback.write("Test Name: {0}\nReceived Points: {1}\nComments: {2}\n"\
                        .format(r["name"],r["points"],r["comments"]))
                feedback.close()

        # Zip up the feedback folder so we can submit it to d2l
        zipFilePath = feedbackDir+'feedback.zip'
        zipf = zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED)
        for f in os.listdir(feedbackDir):
            if f[-3:] == 'txt':
                zipf.write(feedbackDir+f,os.path.basename(feedbackDir+f))
        zipf.close()
        print("Feedback file located at {0} Grab it and upload it to d2l!".format(zipFilePath))

if __name__ == "__main__":
    print("hello!")
