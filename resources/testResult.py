#!/usr/bin/env python3

class ut_result:
    def __init__(self, name="NA", passed=False, maxPoints=10, comments="",\
            points=0):
        self.name = name;       # name of unit test
        self.passed = passed;   # true or false 
        self.maxPoints = int(maxPoints)  # maximum points for test
        self.points = int(points)    # points awarded
        self.comments = comments    # any reasons for passing or failing test

if __name__ == "__main__":
    print("Running self test...")
    c = ut_result()
    attrs = vars(c)
    print('\n'.join("%s: %s" % item for item in attrs.items()))
    print("Done")
