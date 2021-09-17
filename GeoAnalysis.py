import datetime
import dataclasses
import sqlite3
import json
from turfpy.measurement import length
from turfpy.measurement import distance
from geojson import MultiLineString
from geojson import Feature

def seeTHs():
    conn = sqlite3.connect('glaciertrails.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT name FROM Campsites WHERE type = 'Trailhead' ORDER BY name ''' )
    rows = cur.fetchall()
    print(rows)

def getTrails():
    conn = sqlite3.connect('glaciertrails.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT desc FROM Trails ''' )
    rows = cur.fetchall()
    return(rows)

def checkconnected(trail1 : MultiLineString, trail2 : MultiLineString):
    t1coordbeg = json.loads(trail1[0][0])[0][0]
    t1coordend = json.loads(trail1[0][0])[0][len(json.loads(trail1[0][0])[0])-1]
    t2coordbeg = json.loads(trail2[0][0])[0][0]
    t2coordend = json.loads(trail2[0][0])[0][len(json.loads(trail2[0][0])[0])-1]
    
    if distance(t1coordbeg, t2coordbeg, units='mi') < 0.01 or distance(t1coordend, t2coordbeg, units = 'mi') < 0.01:
        print(distance(t1coordbeg, t2coordbeg, units='mi'), ' ', distance(t1coordend, t2coordbeg, units = 'mi'))
        return True
    elif distance(t1coordend, t2coordend, units='mi') < 0.01 or distance(t1coordbeg, t2coordend, units = 'mi') < 0.01:
        print(distance(t1coordend, t2coordend, units='mi'), ' ', distance(t1coordbeg, t2coordend, units = 'mi'))
        return True

def findstartrail(trailheadname : str):
    conn = sqlite3.connect('glaciertrails.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT location FROM Campsites WHERE name = ?''', (trailheadname, ) )
    rows = cur.fetchall()
    thloc = json.loads(rows[0][0])
    for trailname in getTrails():
        #print(len(json.loads(gettrailcoordinates(trailname[0])[0][0])[0])-1)
        trailpoint1 = json.loads(gettrailcoordinates(trailname[0])[0][0])[0][0]
        trailpoint2 = json.loads(gettrailcoordinates(trailname[0])[0][0])[0][len(json.loads(gettrailcoordinates(trailname[0])[0][0])[0])-1]
        #print(trailpoint1, trailpoint2)
        if distance(thloc, trailpoint1, units = 'mi') < 0.05 or distance(thloc, trailpoint2, units = 'mi') < 0.05:
            print(trailname, distance(thloc, trailpoint1, units = 'mi'), distance(thloc, trailpoint2, units = 'mi'))


def gettrailcoordinates(name):
    conn = sqlite3.connect('glaciertrails.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT coordinates FROM Trails WHERE desc = ? ''' , (name,) )
    rows = cur.fetchall()
    return rows

