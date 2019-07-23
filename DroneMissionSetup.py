#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:00:47 2019

@author: ksenator
"""

import pandas


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
