#https://public-nps.opendata.arcgis.com/datasets/glacier-national-park-trails/explore?location=48.818230%2C-113.959516%2C10.04

import datetime

class trip:
    def __init__(self, nights, enterTH, exitTH, startday):
        self.nights = nights
        self.enterTH = enterTH
        self.exitTH = exitTH
        self.startday = startday

KodyTrip = trip(3, 'LTE', 'CHF', datetime.datetime.now())
print(KodyTrip.nights, KodyTrip.enterTH, KodyTrip.exitTH, KodyTrip.startday)
