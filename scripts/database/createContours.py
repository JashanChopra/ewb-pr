"""
This script adds contours to the database
"""

from database.gpxfuncs import loadgpx
from database.databaseFuncs import get_conn, create_contour


def createcontours(gpx, conn):
    """
    This function creates a database entry for each point of each track of a GPX file
    :param gpx: a valid GPX stype list from loadgpx()
    :param conn: an sqlite3 connection to the database
    :return:
    """
    for track in gpx.tracks:                                                            # loop over each track
        for segment in track.segments:                                                  # loop over each segment
            for point in segment.points:                                                # loop over each point
                addpoint = (point.latitude, point.longitude, point.elevation)           # create db entry
                create_contour(conn, addpoint)                                          # add to db

    print(f'Each point of {len(gpx.tracks)} tracks was added to the database')          # final print statement


if __name__ == '__main__':
    db = r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db'                    # database location
    filename = '5ft contours.gpx'                                                       # filename of gpx file
    conn = get_conn(db)                                                                 # create sqlite3 connection
    gpx = loadgpx(filename)                                                             # load gpx file
    createcontours(gpx, conn)                                                           # call createcontours()


