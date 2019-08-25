"""
This script quickly adds the final GPS products to the database for final analysis, it should only be used a single
time. *8/14/2019)
"""

# import libraries
import pandas as pd
import os
from databaseFuncs import get_conn


def adddb(conn):
    # directorys
    maindir = r'C:\Users\jasha\PycharmProjects\ewb-pr'
    datadir = os.path.join(maindir, 'data')
    poidir = os.path.join(datadir, 'final_poi.csv')
    trackdir = os.path.join(datadir, 'final_tracks.csv')

    # import data from csv
    poi = pd.read_csv(poidir)
    track = pd.read_csv(trackdir)

    # loop through poi and add to db
    sql = ''' INSERT INTO poi(name, lat, long, elevation, time, trackname)                 
                  VALUES(?,?,?,?,?, ?) '''  # sql insert statement
    cur = conn.cursor()  # connection cursor


if __name__ == '__main__':
    conn= get_conn(r'C:\Users\jasha\PycharmProjects\ewb-pr\data\gpspoints.db')