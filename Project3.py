#Jared Immerman

import os
import csv
import pymongo
import pandas as pd
import argparse

def timeCode(currentFolder, frameStart, frameEnd):
    frameAmount = 10
    frameRate = 24
    timeS = frameStart / frameRate
    timeE = frameEnd / frameRate

    hours = int(times / 3600)
    minutes = int((time % 3600) / 60)
    seconds = int(time % 60)
    frames = int((time - int(time)) * frameRate)

    return "Time Code: ", hours, minutes, seconds, frames



print("\nSTART\n")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Jareds_db"]

baselightCol = db['Folder_Frames']
xytechCol= db['Workorder_Location']

#argparse arguments
parser = argparse.ArgumentParser(description ='SOMETHING')
parser.add_argument('--baselight', type=argparse.FileType('r'))
parser.add_argument('--xytech', type=argparse.FileType('r'))
parser.add_argument('--process', dest="process", help="Video process")
parser.add_argument('--output', dest="output", help="Parameters for XLS")

args = parser.parse_args()

#read xytech
if args.xytech:
    with args.xytech as f:
        XY_File = f.read().splitlines()

#read baselight
if args.baselight:
    BL_File = args.baselight

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

    #ADDING TO DB
    #adding values to db for baselight
    # baselightCol.insert_one({str(currentFolder) : fixFrames})

    #adding values to db for xytech
    xytechCol.insert_one({'Xytech workorder 1109' : str(currentFolder)})

    tempStart = 0
    tempLast = 0
    for numb in fixFrames:
        csvFile.close()
        #if error found, pop from parseLine
        if not numb.isnumeric():
            continue

        # baselightCol.insert_one({str(currentFolder) : numb})

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
                baselightCol.insert_one({currentFolder : f'{tempStart}-{tempLast}'})
                with open(csvFilename, "a") as csvFile:
                    csvFile.write(f"{currentFolder},")
                    csvFile.write(f" {tempStart}-{tempLast},\n")
            else:
                print(currentFolder, tempStart)
                baselightCol.insert_one({currentFolder : f'{tempStart}'})
                with open(csvFilename, "a") as csvFile:
                    csvFile.write(f"{currentFolder},")
                    csvFile.write(f" {tempStart}\n")
            tempStart = numb
            tempLast = 0
    if int(tempLast) > 0:
        print(currentFolder, tempStart + "-" + tempLast)
        baselightCol.insert_one({currentFolder : f'{tempStart}-{tempLast}'})
        with open(csvFilename, "a") as csvFile:
            csvFile.write(f"{currentFolder},")
            csvFile.write(f" {tempStart}-{tempLast},\n")
    else:
        print(currentFolder, tempStart)
        baselightCol.insert_one({currentFolder : f'{tempStart}'})
        with open(csvFilename, "a") as csvFile:
            csvFile.write(f"{currentFolder},")
            csvFile.write(f" {tempStart},\n")

    timeCode(currentFolder, tempStart, tempLast)

    csvFile.close

#process video file and call db
if args.process:
    print()
    print('db data: ', db.list_collection_names())
    for i in baselightCol.find({},{"_id":0}):
        # timeCode()
        print('Baselight db data: ', i)

    for j in xytechCol.find({},{"_id":0}):
        print('Xytech db data: ', j)
   

baselightCol.drop()
xytechCol.drop()


#python Project3.py --baselight Baselight_export.txt --xytech Xytech.txt --process twitch_nft_demo.mp4
