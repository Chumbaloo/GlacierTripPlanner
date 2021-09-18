import datetime
import dataclasses
import sqlite3
import json
from turfpy.measurement import length
from turfpy.measurement import distance
from geojson import MultiLineString
from geojson import LineString
from geojson import Feature


def seeTHs():
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT name FROM Campsites WHERE type = 'Trailhead' ORDER BY name """)
    rows = cur.fetchall()
    print(rows)


def getTrails():
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT desc FROM Trails """)
    rows = cur.fetchall()
    return rows


def checkconnected(trail1: MultiLineString, trail2: MultiLineString):
    t1coordbeg = json.loads(trail1[0][0])[0][0]
    t1coordend = json.loads(trail1[0][0])[0][len(json.loads(trail1[0][0])[0]) - 1]
    t2coordbeg = json.loads(trail2[0][0])[0][0]
    t2coordend = json.loads(trail2[0][0])[0][len(json.loads(trail2[0][0])[0]) - 1]

    if distance(t1coordbeg, t2coordbeg, units="mi") < 0.01 or distance(t1coordend, t2coordbeg, units="mi") < 0.01:
        print(distance(t1coordbeg, t2coordbeg, units="mi"), " ", distance(t1coordend, t2coordbeg, units="mi"))
        return True
    elif distance(t1coordend, t2coordend, units="mi") < 0.01 or distance(t1coordbeg, t2coordend, units="mi") < 0.01:
        print(distance(t1coordend, t2coordend, units="mi"), " ", distance(t1coordbeg, t2coordend, units="mi"))
        return True


def findstartrail(trailheadname: str):
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT location FROM Campsites WHERE name = ?""", (trailheadname,))
    rows = cur.fetchall()
    thloc = json.loads(rows[0][0])
    for trailname in getTrails():
        # print(len(json.loads(gettrailcoordinates(trailname[0])[0][0])[0])-1)
        trailpoint1 = json.loads(gettrailcoordinates(trailname[0])[0][0])[0][0]
        trailpoint2 = json.loads(gettrailcoordinates(trailname[0])[0][0])[0][
            len(json.loads(gettrailcoordinates(trailname[0])[0][0])[0]) - 1
        ]
        # print(trailpoint1, trailpoint2)
        if distance(thloc, trailpoint1, units="mi") < 0.05 or distance(thloc, trailpoint2, units="mi") < 0.05:
            print(trailname, distance(thloc, trailpoint1, units="mi"), distance(thloc, trailpoint2, units="mi"))


def gettrailcoordinates(name):
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT coordinates FROM Trails WHERE desc = ? """, (name,))
    rows = cur.fetchall()
    return rows


def getvaliddests(point: list):
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT location, name FROM Campsites where type in ('Trailhead','Campground') """)
    rows = cur.fetchall()
    closedests = []
    for row in rows:
        if distance(json.loads(row[0]), point, units="mi") < 16:
            print(row[1])


def findstartrails(point: list):
    trailoptions = []
    thloc = point
    for trailname in getTrails():
        trailpoint1 = json.loads(gettrailcoordinates(trailname[0])[0][0])[0][0]
        trailpoint2 = json.loads(gettrailcoordinates(trailname[0])[-1][-1])[-1][-1]
        # print(trailname[0], trailpoint1, trailpoint2)
        if distance(thloc, trailpoint1, units="mi") < 0.05 or distance(thloc, trailpoint2, units="mi") < 0.05:
            trailoptions.append([trailname[0], json.loads(gettrailcoordinates(trailname[0])[0][0])[0]])
    return trailoptions


def getroutes(start: list, end: list, proutes, routes, stopper, traveled):
    print("******************************************")
    # stopper = stopper + 1

    for segment in findstartrails(start):
        # print(start)
        for trail in findstartrails(start):
            print(trail[0])
        trind = 0
        for s in traveled:
            if s == segment[0]:
                trind = 1
        if trind == 1:
            continue

        traveled.append(segment[0])

        # print(traveled)
        # if stopper == 3:
        #     break

        # print('Current segment: ',segment[0], segment[-1][0], segment[-1][-1])
        # print(len(proutes), segment[0],len(segment[1]))
        if len(proutes) >= len(segment[1]):
            # print(proutes[-len(segment[1])+1], segment)
            if proutes[-len(segment[1]) + 1] == segment:
                print("No Backtracking!")
                continue

        # Check that our length is still < 16 miles
        if length(LineString(segment[1])) > 16:
            print("Route > 16 miles.")
            continue

        # Check if we have arrived!
        if distance(segment[1][0], end) < 0.05 or distance(segment[1][-1], end) < 0.05:
            routes.append(proutes)
            print("made it!")
            # del proutes[-1]
            continue

        if distance(segment[1][0], start) < distance(segment[1][-1], start):
            for item in segment[1]:
                proutes.append(item)
        else:
            revseg = segment[1]
            revseg.reverse()
            for item in revseg:
                proutes.append(item)
        # print(proutes)
        print("___________________________")
        getroutes(proutes[-1], end, proutes, routes, stopper, traveled)

    # for route in routes:
    #     #find both ends of the last trail segment in each route
    #     p1 = route[len(route)-1][1][len(route[0])]
    #     p2 = route[len(route)-1][1][len(route[len(route)-1][1])-1]

    # whichever point is furthest from the last starting point is our new starting point
    # for the next segment
    # print(distance(p1,start,units='mi'))
