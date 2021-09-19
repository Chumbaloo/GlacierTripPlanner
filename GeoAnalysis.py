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
        if distance(thloc, trailpoint1, units="mi") < 0.05 or distance(thloc, trailpoint2, units="mi") < 0.02:
            print(trailname, distance(thloc, trailpoint1, units="mi"), distance(thloc, trailpoint2, units="mi"))


def gettrailcoordinates(name):
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT coordinates FROM Trails WHERE desc = ? """, (name,))
    rows = cur.fetchall()
    return rows

def gettrailcoordinateslist(name):
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT coordinates FROM Trails WHERE desc = ? """, (name,))
    rows = cur.fetchall()
    return json.loads(rows[0][0])[0]

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
        if distance(thloc, trailpoint1, units="mi") < 0.05 or distance(thloc, trailpoint2, units="mi") < 0.02:
            trailoptions.append([trailname[0], json.loads(gettrailcoordinates(trailname[0])[0][0])[0]])
    return trailoptions


def setstart(laststart: list, route: list):
    if distance(laststart, route[0]) > distance(laststart, route[-1]):
        return route[0]
    else:
        return route[-1]


def bfs(start: list):
    queue = [start]
    visited = []
    #visitedname = []
    while queue != []:
        print("Queue: ", queue)
        s = queue.pop(0)
        visited.append(s)
        for branches in findstartrails(s):
            candidate = setstart(s, branches[1])
            trigger = 0
            for v in visited:
                if distance(v, candidate, units="mi") < 0.02:
                    trigger = 1
            if trigger != 1:
                queue.append(candidate)
                #visitedname.append(branches[0])
    return(visited)

def bfs_routes(start: list):
    queue = []
    currentroute = []
    priorloc=start
    for seeds in findstartrails(start):
        queue.append(seeds[0])
    print(queue)
    while queue != []:
        print('Queue: ',queue)
        s = queue.pop(0)
        currentroute.append(s)

        candidate = setstart(priorloc, gettrailcoordinateslist(s))
        for branch in findstartrails(candidate):
            if currentroute[-1] != branch[0]:
                 print(branch[0])
            # else:
            #     1


    # visited = []
    # current_path = []
    # #visitedname = []
    # while queue != []:
    #     print("Queue: ", queue)
    #     s = queue.pop(0)
    #     visited.append(s)
    #     for branches in findstartrails(s):
    #         current_path.append(branches[0])
    #         candidate = setstart(s, branches[1])
    #         trigger = 0
    #         for v in visited:
    #             if distance(v, candidate, units="mi") < 0.02:
    #                 trigger = 1
    #         if trigger != 1:
    #             queue.append(candidate)
    #             #visitedname.append(branches[0])
    # return(visited)