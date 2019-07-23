#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:00:47 2019

@author: ksenator
"""

import os

import mpu
import pandas
import piexif


def DroneMissionPoints(FilePath):
    # Static Variables
    BasePath = r"\Users\capps\PycharmProjects\DroneScripts\litchi_base.csv"
    MissionName = "LitchiHubImport.csv"
    OrderFileName = "PairingData.csv"

    pandas.options.mode.chained_assignment = None  # default='warn'

    # Template setup
    Index = ['latitude', 'longitude', 'altitude(m)', 'heading(deg)', 'curvesize(m)', 'rotationdir', 'gimbalmode',
             'gimbalpitchangle', 'actiontype1', 'actionparam1', 'actiontype2', 'actionparam2', 'actiontype3',
             'actionparam3', 'actiontype4', 'actionparam4', 'actiontype5', 'actionparam5', 'actiontype6',
             'actionparam6', 'actiontype7', 'actionparam7', 'actiontype8', 'actionparam8', 'actiontype9',
             'actionparam9', 'actiontype10', 'actionparam10', 'actiontype11', 'actionparam11', 'actiontype12',
             'actionparam12', 'actiontype13', 'actionparam13', 'actiontype14', 'actionparam14', 'actiontype15',
             'actionparam15', 'altitudemode', 'speed(m/s)', 'poi_latitude', 'poi_longitude', 'poi_altitude(m)',
             'poi_altitudemode', 'photo_timeinterval']
    Values = [0, 0, 0, 0, 0, 0, 0, 0.0, -1, 0, 1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1,
              0, -1, 0, -1, 0, -1, 0, 0, 0, 0.0, 0.0, 0, 0, 0]
    RowTemplate = pandas.Series(Values, Index)

    # Read the csv files then their important data
    Data = pandas.read_csv(FilePath)
    BaseData = pandas.read_csv(BasePath)

    # Here we need to add the header check so that the reads from the data and only pulls the correct spelling of the header

    # Read the specific columns from the data set
    LatList = pandas.Series.to_list(Data.latitude)
    LonList = pandas.Series.to_list(Data.longitude)
    IdList = pandas.Series.to_list(Data.objectid)

    # Zip everything important for renaming together
    ForFileRenaming = sorted(zip(LatList, LonList, IdList))

    # Variables for the loop
    NumberOfPoints = len(LatList)
    NewData = BaseData.head(0)
    i = 0

    # The points of interest are set to each of the input poles and then the new entry is added to a DataFrame
    while i < NumberOfPoints:
        RowTemplate[0] = LatList[i]
        RowTemplate[1] = LonList[i]
        RowTemplate[40] = LatList[i]
        RowTemplate[41] = LonList[i]
        NewData = NewData.append(RowTemplate, ignore_index=True)
        i += 1

    NewData.to_csv(MissionName, header=False, index=False)
    pandas.DataFrame(ForFileRenaming).to_csv(OrderFileName, header=False, index=False)


# DroneMissionPoints("/Users/ksenator/Documents/GitHub/Apps/routePlanner/litchi_mission.csv")

def RenamePictures(FilePath):
    # initialize all the data storage and set the path to where the pictures are #####
    FileNames = os.listdir(FilePath)
    PictureList = []
    LatitudeList = []
    LongitudeList = []
    ##########################################################################################

    # Creates a list of jpeg files in the current directory ##################################
    for file in FileNames:
        if file[len(file) - 3:len(file)] == 'JPG':  # is the file a JPG
            PictureList.append(FilePath + "\\" + file)  # if it is, put it in the list of pictures
    ##########################################################################################

    # Loads in images and finds the GPS data #################################################
    for picture in PictureList:
        # PicturePath = FilePath + "\\" + picture
        # ExifInfoOne = piexif.load(PicturePath)
        ExifInfoOne = piexif.load(picture)
        LocationInfo = ExifInfoOne["GPS"]

        # Latitude conversion ####################################################################
        NorthSouth = LocationInfo[1]
        LatDMS = LocationInfo[2]
        i = 0
        for ratio in LatDMS:
            i += 1
            if i == 1:
                Degree = float(ratio[0]) / float(ratio[1])
            elif i == 2:
                Minute = float(ratio[0]) / float(ratio[1])
            else:
                Second = float(ratio[0]) / float(ratio[1])
        ##########################################################################################
        Latitude = dms2dd(Degree, Minute, Second, NorthSouth)

        # Longitude conversion ###################################################################
        EastWest = LocationInfo[3]
        LonDMS = LocationInfo[4]
        i = 0
        for ratio in LonDMS:
            i += 1
            if i == 1:
                Degree = float(ratio[0]) / float(ratio[1])
            elif i == 2:
                Minute = float(ratio[0]) / float(ratio[1])
            else:
                Second = float(ratio[0]) / float(ratio[1])
        #########################################################################################
        Longitude = dms2dd(Degree, Minute, Second, EastWest)

        LatitudeList.append(Latitude)
        LongitudeList.append(Longitude)

    # This is the data from the route planner that gets carried over.
    Data = pandas.read_csv("/Users/capps/Desktop/pics/PairingData.csv")
    LatitudesFromData = pandas.Series.to_list(Data.iloc[:, 1])
    LongitudesFromData = pandas.Series.to_list(Data.iloc[:, 0])
    ObjectIDFromData = pandas.Series.to_list(Data.iloc[:, 2])

    PairsOfPoleLocations = zip(LatitudesFromData, LongitudesFromData)

    # Now let's turn the zipped lists into lists of lists (easier to loop through and index)############################
    PairsOfData = []
    PairsOfMetadata = zip(LatitudeList, LongitudeList)
    for pairs in PairsOfMetadata:
        PairsOfData.append(pairs)

    PairsOfPoles = []
    for pairs in PairsOfPoleLocations:
        PairsOfPoles.append(pairs)
    ###################################################################################################################

    ImageID = []
    # Now let's go through all the pairs and find their closest neighbor of all of the points of interest and change the name of the image according to the object id of the closest match ##################################################
    for pair in PairsOfData:
        # first we have to compare the pair to each pair of latitude and longitude in the data in the data held over from the route planner import
        i = 0
        Option = 0
        MinDistance = 1000
        for potentialMatch in PairsOfPoles:  # every picture needs to go through all of the possible poles
            AbsDistance = mpu.haversine_distance(pair, potentialMatch)  # distance between them
            if AbsDistance < MinDistance:  # as you go through the poles, set the closest one as the one to match with
                Option = i
                MinDistance = AbsDistance  # update min distance
            i += 1
        ImageID.append(Option)  # add the objectid number to a list that corresponds to the picture list
    ####################################################################################################################

    # now, as we are going through and naming the pictures, the letter to be appended needs to update depending on each unique objectid ####################################################################################################
    TempDict = dict.fromkeys(ObjectIDFromData, 0)  # makes dictionary of the objectids, sets their values to zero
    WhatLetterToPick = []
    for key, value in TempDict.items():  # turn that dictionary into a list of lists
        Temp = [key, value]
        WhatLetterToPick.append(Temp)

    Alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag']
    EndString = ".JPG"
    i = 0
    while i < len(ImageID):
        OutString = str(WhatLetterToPick[ImageID[i]][0]) + "_" + Alphabet[WhatLetterToPick[ImageID[i]][1]] + EndString
        print(OutString)
        os.rename(PictureList[i], os.path.join(FilePath, OutString))
        WhatLetterToPick[ImageID[i]][1] += 1
        i += 1


def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (3600)
    if direction == b'W' or direction == b'S':
        dd *= -1
    return dd

# RenamePictures(r'C:\Users\capps\Desktop\pics')
