import turfpy
import sqlite3
import geojson
import json

from turfpy.measurement import length
from turfpy.measurement import distance
from geojson import MultiLineString
from geojson import Feature

#The trail coordinates in the glaciertrails SQL database are multi-line-strings.
#In most cases, this is irrelevant, since the multi-line-string just
#contains a single line-string. In some cases, the MLS contains
#multiple LS. This seems to happen when there is a branch-off at
#some point mid-trail.

#This code will identify all records where the MLS contains multiple LS.
#Then, it will split these records as two separate trails.
#This is how the rest of the program expects the data to be formatted.

if __name__ == "__main__":
    conn = sqlite3.connect("glaciertrails.sqlite")
    cur = conn.cursor()

    cur.execute("""SELECT * FROM Trails""")
    rows = cur.fetchall()

    for row in rows:
        coordsMLS = json.loads(row[-1])
        if len(coordsMLS) > 1:
            
            print(len(coordsMLS))
            print('----------------------------------------------------------')
            
            index = 0

            for l in coordsMLS:
                coordsin=('['+json.dumps(coordsMLS[index])+']')
                descin = row[1]+' - segment '+str(index+1)
                subdistin = row[2]
                milesin = -999
                metersin = -999
                calcmilesin = -999

                print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                index = index+1
                cur.execute(
                """INSERT INTO Trails (desc, subdist, miles, meters, calcmiles, coordinates)
                VALUES ( ?, ?, ?, ?, ?, ?)""",
                (descin, subdistin, milesin, metersin, calcmilesin, coordsin),
                )

            cur.execute(
            """DELETE FROM Trails WHERE id = """+str(row[0]))

    conn.commit()

    cur.execute("""SELECT * FROM Trails""")
    rows = cur.fetchall()
    for row in rows:
        print(row[0])
        coordsMLS = json.loads(row[-1])
        ls = MultiLineString(json.loads(row[-1]))
        f = Feature(geometry=ls)
        calcmiles = length(f, units="mi")
        cur.execute(
            """Update Trails """+"SET calcmiles ="+str(calcmiles)+","+"miles ="+str(calcmiles)+" WHERE id = "+str(row[0])
            
        )
    conn.commit()

    cur.execute("""SELECT * FROM Trails""")
    rows = cur.fetchall()
    for row in rows:
        if row[3] < 0.02:
            cur.execute(
            """DELETE FROM Trails WHERE id = """+str(row[0]))
    conn.commit()