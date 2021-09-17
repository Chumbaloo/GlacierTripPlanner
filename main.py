#https://public-nps.opendata.arcgis.com/datasets/glacier-national-park-trails/explore?location=48.818230%2C-113.959516%2C10.04

import datetime
import dataclasses
import sys
import json
from Trip import trip
import GeoAnalysis

if __name__=='__main__':
    KodyTrip = trip()
    
    #Find all trail segments that are connected to the given trail segment
    trailname1 = 'Granite Park Chalet - Switfcurrent Pass Tr Jct'
    t1 = GeoAnalysis.gettrailcoordinates(trailname1)
    for trailname2 in GeoAnalysis.getTrails():
        if GeoAnalysis.gettrailcoordinates(trailname2[0]) == t1:
            continue
        else:
            if GeoAnalysis.checkconnected(t1,GeoAnalysis.gettrailcoordinates(trailname2[0])):
                print(trailname2[0]+'\n'+trailname1)

    # while(True):
    #     selectnights = input('How many nights will the trip last?')
    #     try:
    #         KodyTrip.addNights(int(selectnights))
    #         break
    #     except:
    #         if selectnights == 'exit':
    #             sys.exit()
    #         else:
    #             print('Please enter an integer value of 1 to 15. Enter exit to close.')
    #             continue

    # while(True):
    #     selectenterth = input('Enter entrance trailhead')
    #     try:
    #         KodyTrip.addEnterTH(selectenterth)
    #         break
    #     except:
    #         if selectenterth == 'exit':
    #             sys.exit()
    #         elif selectenterth == 'options':
    #             GeoAnalysis.seeTHs()
    #         else:
    #             print('Please enter a valid trailhead. Enter exit to close. Enter options to see a list of valid trailheads.')
    #             continue


    # print(KodyTrip.nights, KodyTrip.enterth)
