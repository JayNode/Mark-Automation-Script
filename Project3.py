#Jared Immerman

import os
import csv
import pymongo
import pandas as pd
import argparse

print("\nSTART\n")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Jared-db"]

baselightCollection = db['Folder/Frames']
xytechCollection = db['Workorder/Location']

#argparse arguments
parser = argparse.ArgumentParser(description ='SOMETHING')
parser.add_argument('--baselight', type=argparse.FileType('r'))
parser.add_argument('--xytech', type=argparse.FileType('r'))
parser.add_argument('--process', type=bool)
# parser.add_argument('--output')

args = parser.parse_args()

#read xytech
if args.xytech:
    with args.xytech as f:
        XY_File = f.read().splitlines()

#read baselight
if args.baselight:
    BL_File = args.baselight
    baselightCollection = BL_File

csvFilename = "fix_these.csv"
with open(csvFilename, "w") as csvFile:
    csvFile.write("Producer,Operator,Job,Notes\n")
    csvFile.write("Olivia Rodrigo, Johnny Bananas, Dirtfixing, Please clean files noted per Colorist Brock Purdy\n\n")
    csvFile.write("Locations, Frames\n")
csvFile.close()

print(XY_File)


for currentReadLine in BL_File:
    
    #print currentReadLine
    print("\nCurrent read: " + currentReadLine)

    #parse currentReadLine
    fixFrames = currentReadLine.split()
    print("Parsed Line: ", fixFrames)

    #pop file location from parseLine
    currentFolder = fixFrames.pop(0)
    #parse folder
    parseFolder = currentFolder.split("/")
    #pop system location from parseFolder
    parseFolder.pop(1)
    #merge parseFolder with file location layout
    newFolder = "/".join(parseFolder)

    print("parseFolder: ", parseFolder)
    print("newfolder: ", newFolder)

    for techFile in XY_File:
        #if folder from BL matches folder from Xytech, make currentFolder
        if newFolder in techFile:
            currentFolder = techFile.strip()
            print("Current Folder: ", currentFolder)

    print("Fix Frames: " , fixFrames)

    tempStart = 0
    tempLast = 0
    count = 0
    for numb in fixFrames:
        csvFile.close()
        #if error found, pop from parseLine
        if not numb.isnumeric():
            continue
        count += 1
        #for numbers that are in a row
        if tempStart == 0:
            tempStart = numb
            continue
        #if numb is start + 1, set last = numb
        if numb == str(int(tempStart) + 1) or numb == str(int(tempLast) + 1):
            tempLast = numb
            continue
        #check if numb is greater than last + 1
        elif int(numb) > (int(tempLast) + 1):
            if int(tempLast) > 0:
                print(currentFolder, tempStart + "-" + tempLast)
                with open(csvFilename, "a") as csvFile:
                    csvFile.write(f"{currentFolder},")
                    csvFile.write(f" {tempStart}-{tempLast},\n")
            else:
                print(currentFolder, tempStart)
                with open(csvFilename, "a") as csvFile:
                    csvFile.write(f"{currentFolder},")
                    csvFile.write(f" {tempStart}\n")
            tempStart = numb
            tempLast = 0
    if int(tempLast) > 0:
        print(currentFolder, tempStart + "-" + tempLast)
        with open(csvFilename, "a") as csvFile:
            csvFile.write(f"{currentFolder},")
            csvFile.write(f" {tempStart}-{tempLast},\n")
    else:
        print(currentFolder, tempStart)
        with open(csvFilename, "a") as csvFile:
            csvFile.write(f"{currentFolder},")
            csvFile.write(f" {tempStart},\n")

    csvFile.close

#python3 Project3.py --baselight Baselight_export.txt --xytech Xytech.txt --process True
