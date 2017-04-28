import subprocess

def compile_make(workingPath):
    output = subprocess.run(['make', '-C', workingPath], stdout=subprocess.PIPE\
            ,stderr=subprocess.PIPE)
    return output

def compile_gcc(targetFilePaths, outputPath=""):
    args = ['gcc']
    for f in targetFilePaths:
        args.append(f)
    if outputPath != "":
        args.append('-o')
        args.append(outputPath)
        
    output = subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return output

def compile_gpp(targetFilePaths, outputPath=""):
    args = ['g++']
    for f in targetFilePaths:
        args.append(f)
    if outputPath != "":
        args.append('-o')
        args.append(outputPath)
        
    output = subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return output

def run_no_input(exePath, exeArgs, outputFile):
    args = []
    args.append(exePath)
    for a in exeArgs:
        args.append(a)

    return subprocess.run(a, encoding="utf-8", stdout=outputFile, \
            stderr=subprocess.PIPE)

def run_with_input(exePath="", exeArgs=[], outputFile="", inputFile=""):
    args = []
    args.append(exePath)
    for a in exeArgs:
        args.append(a)

    return subprocess.run(args, encoding="utf-8", stdout=outputFile, \
            stderr=subprocess.PIPE, stdin=inputFile)

