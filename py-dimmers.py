'''
py-dimmers reads lines from serial port and drives dimmer modules over HTTP
'''

from dimmer import Dimmer
import requests
import json
from os import listdir
from os.path import isfile

dimmers = {}

def readLine() :
    return input()

def processLine(line) :
    arr = line.split('=')
    if len(arr) == 2:
        dimNum = int(arr[0])
        dimVal = int(arr[1])
        processDimmer(dimNum, dimVal)

def processDimmer(dimNum, dimVal) :
    if not dimNum in dimmers: return

    dimmerInstance = dimmers[dimNum]
    for dimAddr in dimmerInstance.addresses:
        dimmerHttp(dimAddr, dimmerInstance.map(dimVal))

def readDimmerConfig():
    dimmerSubDirs = listdir('./dimmers')
    for subDir in dimmerSubDirs:
        if not isfile(subDir) and is_integer(subDir):
            dimIdx = int(subDir)
            theDim = readSingleDimmerConfig('./dimmers/' + subDir)
            dimmers[dimIdx] = theDim

def readSingleDimmerConfig(dimmerSubDir) :
    dim = Dimmer()
    dim.readAddresses(dimmerSubDir + '/addresses.txt')
    dim.readMapping(dimmerSubDir + '/mapping.txt')
    return dim

def dimmerHttp(address, dimVal):
    burning = 1
    if dimVal == 0: burning = 0

    parameters = { 'burn' : burning, 'red' : dimVal }
    jsonData = json.dumps(parameters)

    try:
        requests.post(address, jsonData, timeout=0.2)
    except:
        print('Can\'t connect to ' + address)

def is_integer(str):
    try:
        int(str)
    except ValueError:
        return False
    else:
        return True


'''
Main program
'''
readDimmerConfig()

while True:
    line = readLine()
    processLine(line)
