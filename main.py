# https://public-nps.opendata.arcgis.com/datasets/glacier-national-park-trails/explore?location=48.818230%2C-113.959516%2C10.04

import datetime
import dataclasses
import sys
import json
from Trip import trip
import GeoAnalysis

if __name__ == "__main__":

    GeoAnalysis.bfs_routes([-113.78081, 48.745652])
