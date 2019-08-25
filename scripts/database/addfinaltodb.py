"""
This script quickly adds the final GPS products to the database for final analysis, it should only be used a single
time. *8/14/2019)
"""

# import libraries
import pandas as pd
import os
from databaseFuncs import get_conn, create_meter


def adddb(conn):
    # directorys
    maindir = r'C:\Users\jasha\PycharmProjects\ewb-pr'
    datadir = os.path.join(maindir, 'data')
    poidir = os.path.join(datadir, 'final_poi.csv')
    trackdir = os.path.join(datadir, 'final_tracks.csv')
    meterdir = os.path.join(datadir, 'Puntos GPS metros Mulas.xlsx')

    # import data from csv
    poi = pd.read_csv(poidir)
    track = pd.read_csv(trackdir)
    meter = pd.read_excel(meterdir)

    # loop through poi and add to db
    for i in range(len(meter)):
        create_meter(conn, meter[i])
    print('Meter Points added to database')


if __name__ == '__main__':
    conn = get_conn(r'C:\Users\jasha\PycharmProjects\ewb-pr\data\gpspoints.db')