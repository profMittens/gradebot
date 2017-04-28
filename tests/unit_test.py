import logging
from tools.log import logMsg

'''
    When the test modules are imported they automatically call register_test
    which adds them to this list. Gradebot then uses this list to determine
    what modules to execute
'''
registered_tests = {}
def register_test(name, test):
    registered_tests[name] = test

'''
    A class which defines the results of a unit test. This is returned from the
    unit test run() function and is used to generate the assignment feedback
    and grade files
'''
class ut_result:
    def __init__(self, name="NA", passed=False, maxPoints=10, comments="",\
            points=0):
        self.name = name;       # name of unit test that was ran
        self.passed = passed;   # true or false 
        self.maxPoints = int(maxPoints)  # maximum points for test
        self.points = int(points)    # points awarded
        self.comments = comments    # any reasons for passing or failing test

'''
    A class which defines an individual unit test and its various attributes.
    The unit tests which users right should inherit from this class.
'''
class ut_test:
    def __init__(self, config, maxPoints=10, name="Unit_Test"):
        self.config = config
        self.name = name
        self.result = ut_result(name,False,maxPoints)
        self.inputDir = ""
        self.outputDir = ""
        self.outputFilePath = ""
        self.subDir = "" 

    '''
        Construct the paths the unit test will use, mainly the input and output
        folders where unit test data can be saved at
    '''
    def constructPaths(self,submission):
        self.subDir = submission.workingPath
        self.inputDir = self.config.dir_tests+'/'+self.config.aid
        self.outputDir = self.config.dir_output+'/'+self.config.aid+\
                             '/unit_test_output'
        self.outputFilePath = self.outputDir+'/{0}_{1}.txt'.format(self.name,\
                submission.student.sid)
        
    '''
        Place holder function that should be overridden by the child unit test
        class that will be doing the actual work
    '''
    def run(self, submission):
      logMsg(self.config, "Running unit test: "+self.name)
      return self.result


