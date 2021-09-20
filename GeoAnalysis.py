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
    # visitedname = []
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
                # visitedname.append(branches[0])
    return visited


def getroutelength(route: list):
    SQLqstr = ""
    for r in route:
        SQLqstr = SQLqstr + "'" + r + "',"
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT sum(miles) FROM Trails where desc in (""" + SQLqstr + "'ignoreme')")
    rows = cur.fetchall()
    return rows[0][0]


def isrepeat(routes: list, candidate: list):
    for r in routes:
        if r == candidate:
            return True
    return False


def isdeadend(starting: list):
    if len(findstartrails(starting)) == 1:
        return True
    return False


def bfs_routes(start: list, end: list):
    #iteration 12 is having problems! Look there when starting this again... it should be ident as allrepeating
    fml = 0
    successfulroutes = []
    allroutes = []
    queue = []
    currentroute = []
    for seeds in findstartrails(start):
        queue.append(seeds[0])
    while queue != []:
        print("-----------------Iteration Start!-----------------------")
        print("iteration: ", fml)
        # print('Start coords: ',start)
        # print("queue:", queue)
        if fml > 20:
            break
        # From the current route that is entering this iteration, have we traveled all valid paths?
        # If so, chop off last segment of current route and reiterate
        if currentroute != []:
            counter = 0
            repeats = 0
            # print('Current Route: ',currentroute)
            for o in findstartrails(start):
                print(o[0])
                counter = counter + 1
                testroute = currentroute[:]
                testroute.append(o[0])
                if isrepeat(allroutes, testroute):
                    repeats = repeats + 1
            print('Repeats: ', repeats)
            print('Counter: ', counter)
            print(start)
            if counter > 0 and counter == repeats + 1:
                print("all repeat!")
                del currentroute[-1]
                start = setstart(start, gettrailcoordinateslist(currentroute[-1]))
                continue

        # Add next path in queue to the current route
        # We do this before making any other validity checks
        s = queue.pop(0)
        currentroute.append(s)

        print(type(currentroute), currentroute)

        # add current route under review to list of all routes that have been considered
        allroutes.append(currentroute[:])

        if (
            distance(setstart(start, gettrailcoordinateslist(currentroute[-1])), end, units="mi") < 0.02
            and getroutelength(currentroute) < 10
        ):
            print("Arrived")
            successfulroutes.append(currentroute[:])
            del currentroute[-1]
            start = setstart(start, gettrailcoordinateslist(currentroute[-1]))
            fml = fml + 1
            continue

        elif getroutelength(currentroute) > 10:
            del currentroute[-1]
            start = setstart(start, gettrailcoordinateslist(currentroute[-1]))
            print("length!")
            fml = fml + 1
            continue

        elif isrepeat(allroutes[0:-1], currentroute):
            del currentroute[-1]
            start = setstart(start, gettrailcoordinateslist(currentroute[-1]))
            print("repeat!")
            fml = fml + 1
            continue

        elif isdeadend(setstart(start, gettrailcoordinateslist(currentroute[-1]))):
            del currentroute[-1]
            start = setstart(start, gettrailcoordinateslist(currentroute[-1]))
            print("dead end!")
            fml = fml + 1
            continue

        for i in findstartrails(setstart(start, gettrailcoordinateslist(s))):
            if i[0] != currentroute[-1]:
                queue.insert(0, i[0])

        start = setstart(start, gettrailcoordinateslist(s))
        fml = fml + 1
        print("-----------------Iteration End!-----------------------")
    print(successfulroutes)