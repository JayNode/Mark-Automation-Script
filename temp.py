#Jared Immerman

import os
import csv
import pymongo
import pandas as pd
import argparse

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Jared-db"]

baselightCollection = db['Folder/Frames']
xytechCollection = db['Workorder/Location']

def sendXytechToDB(collection, FILE):
    with open(FILE, 'r') as f:
        XY_File = f.read().splitlines()
        for row in XY_File:
            collection.insert_one(row)

def sendBaselightToDB(collection, FILE):
    BL_File = open(FILE, 'r')
    for row in BL_File:
        collection.insert_one(row)

def main():
    
    print("\nSTART\n")

    baselightCollection = db['Folder/Frames']
    xytechCollection = db['Workorder/Location']

    #argparse arguments
    parser = argparse.ArgumentParser(description ='SOMETHING')
    parser.add_argument('--baselight', metavar=('FILE'))
    parser.add_argument('--xytech', metavar=('FILE'))

    args = parser.parse_args()

    #read xytech, send to db
    if args.xytech:
        # with open(args.xytech, 'r') as f:
        #     XY_File = f.read().splitlines()
        xytechCollection = db[args.xytech[0]]
        sendXytechToDB(xytechCollection, args.xytech[1])


    #read baselight, send to db
    if args.baselight:
        # BL_File = open(args.baselight, 'r')
        baselightCollection = db[args.baselight[0]]
        sendBaselightToDB(baselightCollection, args.baselight[1])

    print(xytechCollection)
    print(baselightCollection)

if __name__ == '__main__':
    main()