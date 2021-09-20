import turfpy
import sqlite3
import geojson
import json

from turfpy.measurement import length
from geojson import MultiLineString
from geojson import Feature

if __name__ == "__main__":
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()

    # I should redo this using keys for subdist and type columns since
    # they repeat
    cur.executescript(
        """

    DROP TABLE IF EXISTS Trails;
    DROP TABLE IF EXISTS Campsites; 

    CREATE TABLE Trails (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        desc   TEXT,
        subdist   TEXT,
        miles   FLOAT,
        meters   FLOAT,
        calcmiles   FLOAT,
        coordinates   TEXT
    );

   CREATE TABLE Campsites (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT,
        type   TEXT,
        location   TEXT

    );

    """
    )

    f = open("Glacier_National_Park_Trails.geojson")
    gj = geojson.load(f)
    features = gj["features"]
    # print(features)

    for feature in features:

        desc = feature["properties"]["DESC_SEG"]
        subdist = feature["properties"]["SUBDIST"]
        miles = feature["properties"]["Miles"]
        meters = feature["properties"]["Meters"]
        ls = MultiLineString(feature["geometry"]["coordinates"])
        f = Feature(geometry=ls)
        calcmiles = length(f, units="mi")
        coordinates = json.dumps(feature["geometry"]["coordinates"])

        cur.execute(
            """INSERT INTO Trails (desc, subdist, miles, meters, calcmiles, coordinates)
            VALUES ( ?, ?, ?, ?, ?, ?)""",
            (desc, subdist, miles, meters, calcmiles, coordinates),
        )

    f = open("Glacier_National_Park_Points_of_Interest.geojson")
    gj = geojson.load(f)
    features = gj["features"]
    for feature in features:
        if feature["properties"]["POITYPE"] == "Campground" or feature["properties"]["POITYPE"] == "Trailhead":
            name = feature["properties"]["POINAME"]
            type = feature["properties"]["POITYPE"]
            location = json.dumps(feature["geometry"]["coordinates"])
            cur.execute(
                """INSERT INTO Campsites (name, type, location)
                VALUES ( ?, ?, ? )""",
                (name, type, location),
            )

    conn.commit()
