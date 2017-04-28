#!/usr/bin/env python3
import json
from resources.student import studentHelper
from tests.unit_test import ut_result

class submissionHelper:
    def __init__(self, student=studentHelper(), date="", path="", scomments="",\
            icomments="", maxPoints=0, totalPoints=0):
        self.student = student
        self.date = date
        self.path = path
        self.workingPath = "NA"
        self.studentComments = scomments
        self.instructorComments  = icomments
        self.maxPoints = maxPoints
        self.totalPoints = totalPoints
        self.results = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def save(self, path):
        saveFile = path + '/{0}-{1}-{2}.json'.format(self.student.sid,\
                self.student.fName, self.student.lName)
        with open(saveFile, 'w') as fp:
                fp.write(self.toJSON())

if __name__ == "__main__":
    print("Running self test...")
    c = submissionHelper()
    attrs = vars(c)
    print('\n'.join("%s: %s" % item for item in attrs.items()))
    print("Done")
