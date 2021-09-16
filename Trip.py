import datetime
import dataclasses
import sqlite3
import json

# @dataclasses.dataclass
class trip:
    def addNights(self, nights: int):
        if nights > 15:
            print('Maximum of 15 nights allowed')
            raise ValueError
        elif nights < 1:
            print('At least one night required')
            raise ValueError
        else:
            trip.nights = nights
    
    def addEnterTH(self, enterth: str):
        conn = sqlite3.connect('glaciertrails.sqlite')
        cur = conn.cursor()

        cur.execute('''SELECT name FROM Campsites WHERE type = 'Trailhead' ''' )
        rows = cur.fetchall()
        thlist = []
        for row in rows:
            thlist.append(row[0])
        if enterth not in thlist:
            print('Not a valid entrance point')
            raise ValueError
        else:
            trip.enterth = enterth

    def seeTHs(self):
        conn = sqlite3.connect('glaciertrails.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT name FROM Campsites WHERE type = 'Trailhead' ORDER BY name ''' )
        rows = cur.fetchall()
        print(rows)
