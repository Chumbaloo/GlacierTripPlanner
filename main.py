# https://public-nps.opendata.arcgis.com/datasets/glacier-national-park-trails/explore?location=48.818230%2C-113.959516%2C10.04

import datetime
import dataclasses
import sys
import json
from Trip import trip
import GeoAnalysis

if __name__ == "__main__":
    KodyTrip = trip()
    routes = []
    proutes = []
    traveled = []
    # print(GeoAnalysis.findstartrails([-113.861504, 48.85251]))
    stop = 0
    #GeoAnalysis.getroutes([-114.202083, 48.831028], [-114.120686, 48.904327], proutes, routes, stop, traveled)
    for i in GeoAnalysis.findstartrails([-114.195088, 48.83759]):
        print(GeoAnalysis.findstartrails([-114.195088, 48.83759])[0][0])
    #test
    # GeoAnalysis.findstartrails([-113.78081, 48.745652])

    # #Find all trail segments that are connected to the given trail segment
    # trailname1 = 'Granite Park Chalet - Switfcurrent Pass Tr Jct'
    # t1 = GeoAnalysis.gettrailcoordinates(trailname1)
    # for trailname2 in GeoAnalysis.getTrails():
    #     if GeoAnalysis.gettrailcoordinates(trailname2[0]) == t1:
    #         continue
    #     else:
    #         if GeoAnalysis.checkconnected(t1,GeoAnalysis.gettrailcoordinates(trailname2[0])):
    #             print(trailname2[0]+'\n'+trailname1)

    # #Given a trailhead, find the first trail segment
    # GeoAnalysis.findstartrail('Waterton Valley')

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
