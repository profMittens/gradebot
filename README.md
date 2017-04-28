# Gradebot  
## What is it?  
Gradebot is just a friendly little python bot that is meant to help you automate
the grading process. It is a simple framework that lets you pick where your assignments
are comming from(such as a CMS like D2L or on some git server), download them,
automatically run some set of unit tests on them, save the results of the tests,
and eventually allow you to automatically submit grades back to your learning
management utility such as D2L or Blackboard.

## Dependencies
* python3

## Workflow
1. Create the assignment folders using some assignment identifier. Gradebot recognizes
this as the `aid` parameter. `aid` will be the name of the folders that gradebot
looks for to find submissions, unit tests, and output directories.

    ```./gradebot -c <aid>```

2. Build the unit tests to run against each assignment. All unit tests for your
assignment can be found in `tests/<aid>`. The previous step will have created
this folder for you and copied in a template unit test as well as a template 
\_\_init\_\_.py. Each unit test will consist of a python module inside of the 
folder which imports and runs a `register_test` method which allows the test to 
auto register itself with Gradebot. Each module should define a class which takes 
a `config` object in its constructor and exposes a `run` method which takes a 
`submission` object as a parameter. Each `run` method should return a `ut_result` 
object. Once the module has been written it should be added to the \_\_init\_\_.py 
file. If it is not Gradebot will not run the module.

3. If using D2L download your dropbox submissions and extract the contents into
`submissions/<aid>`. The D2L module expects the students to have submitted a zip
file, if this is not how you require submissions it will need to be modified.  

4. Run gradebot  
   ```./gradebot -dp <dataprovider> -a <aid>```
Gradebot writes an overall log to `output/gradebot.log` and also writes json 
files to `output/<aid>/<studentid>.json`. These files contain the results of each
unit test as well as any auto generated comments you may have put in the tests.
From this point you can go back and manually review any interesting tests and
make modifications to grades and comments.

5. If run with the '''-g''' flag, entries will be added to a gradebook csv file
that can be configured in the `config.ini` file. Currently this file follows
the format that D2L accepts. If using D2L you should export your initial gradebook
to a csv file and use that as your grade file. As assignments are graded this 
file can then be reuploaded to D2L for automatic grade importing. Gradebot will
need to be tweaked to work with other grading systems for automatic grading.

6. When gradebot is run with `-g` it will also generate feedback text files which
are found at `/output/<aid>/feedback`. This directory contains individual text 
files as well as a zip file which can be imported into D2l for bulk uploading
of feedback.

## Interesting file locations  
* `resources/` - contains most of the object type definitions such as submission
and ut_result
* `tools/` - contains data provider modules for d2l and other general utility 
classes

## Gradebot options  
* `-dp` | Dataprovider, valid options are d2l, bb, gh, gl
* `-a`  | aid, id of the assignment to create
* `-d`  | enalbe debug prints
* `-c` <aid> | create entries for an assignment
* `-r` <aid> | remove folders and contents for a specific assignment
* `-g` | generate feedback files which can be uploaded to d2l
* `-ng` | Do not auto grade files, can be used in conjunction with `-g` to generate
grades and feedback after manual review
