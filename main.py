# https://public-nps.opendata.arcgis.com/datasets/glacier-national-park-trails/explore?location=48.818230%2C-113.959516%2C10.04

import datetime
import dataclasses
import sys
import json
from Trip import trip
import GeoAnalysis

if __name__ == "__main__":
    # GeoAnalysis.getroutelength(['Sperry Chalets - Sperry CG','Mt Brown Tr Jct - Snyder Lake Tr Jct'])
    GeoAnalysis.bfs_routes([-113.78081, 48.745652], [-113.799369, 48.750986])
