#!/usr/bin/env python3
import gbconfig
import logging
from tests.unit_test import register_test
from tests.unit_test import ut_test
from tools.log import logMsg

'''
    Define your unit test by creating a class which inherits from ut_test. In 
    the super constructor be sure to pass in the config file, the max points
    this unit test would be worth, and the name of the unit test. 

    Once your class is created be sure to define the run function which will
    be the code that is executed by Gradebot and contains your unit test logic.

    The last line in your file should also call register_test which will register
    your class with Gradebot to be executed.

    A final step is to import your class in the __init__.py file so the
    register_test() function is automatically run when Gradebot calls

        from <aid> import *

    which kickstarts the registration process
'''
class ut_template(ut_test):
    def __init__(self, config):
        super().__init__(config, 10, "Test Template")
        self.config = config
        self.result.passed = True

    # Define your unit test here
    def run(self, submission):
        logMsg(self.config, "Running unit test")
        return self.result 

# Register this unit test with gradebot
register_test("template",ut_template)
