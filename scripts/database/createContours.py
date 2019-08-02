"""
This script adds contours to the database
"""

from database.gpxfuncs import loadgpx
from database.databaseFuncs import get_conn, create_contour


def createcontours(gpx, conn):
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                addpoint = (point.latitude, point.longitude, point.elevation)
                create_contour(conn, addpoint)

    print(f'Each point of {len(gpx.tracks)} tracks was added to the database')


if __name__ == '__main__':
    db = r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db'
    filename = '5ft contours.gpx'
    conn = get_conn(db)
    gpx = loadgpx(filename)
    createcontours(gpx, conn)


