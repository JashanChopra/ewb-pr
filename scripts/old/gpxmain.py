"""
This script is the central script to run for taking new data GPX files and adding them to the database. Documentation
for it can be found in the Puerto Rico Google Drive under the 2018-2019 --> Subteams --> Design folder
"""

# import libraries
from database.gpxfuncs import loadgpx, loadgpxfiles
from old.databaseFuncs import create_poi, get_conn, create_contour
import shutil
import os


def append_names(conn, newfiles):
    """
    This script guides the user to change the names of points of interest and then updates the database, it takes
    no inputs. Run this python file to append names for any given script.
    :param conn: a valid sqlite3 connection
    :param newfiles: a list of valid gpx filenames
    """

    # ask the user to enter filename, repeat until correct

    for filename in newfiles:
        try:
            gpx = loadgpx(filename)
            print(f'{filename} read properly')
            print('*------------*')
        except FileNotFoundError as error:
            print(f'{filename} not found in directory, try again')
            pass

        for waypoint in gpx.waypoints:
            namechange = input(f'Do you want to change the name of waypoint {waypoint.name}? [y/n]: ')

            if namechange == 'y':
                waypoint.name = input('Enter the new name of the waypoint: ')
                print(f'The new name of this waypoint is {waypoint.name}')
                print('*------------*')

            else:
                print(f'The waypoint name will stay as {waypoint.name}')
                print('*------------*')

            addpoint = (waypoint.name, waypoint.latitude,
                        waypoint.longitude, waypoint.elevation,
                        waypoint.time, gpx.tracks[0].name)

            idx = create_poi(conn, addpoint)
            print(f'{waypoint.name} has been added to the database with id {idx}')


def createcontours(conn, newfiles):
    """
    This function creates a database entry for each point of each track of a GPX file
    :param newfiles: a list of valid gpx filenames in the given directory
    :param conn: an sqlite3 connection to the database
    :return:
    """
    for filename in newfiles:
        try:
            gpx = loadgpx(filename)
            print(f'{filename} read properly')
            print('*------------*')
        except FileNotFoundError as error:
            print(f'{filename} not found in directory, try again')
            pass

        print('Adding each point in track, this may take a moment')
        for track in gpx.tracks:                                                            # loop over each track
            for segment in track.segments:                                                  # loop over each segment
                for point in segment.points:                                                # loop over each point
                    addpoint = (point.latitude, point.longitude, point.elevation,
                                gpx.tracks[0].name)                                         # create db entry
                    create_contour(conn, addpoint)                                          # add to db

        print(f'Each point of {gpx.tracks[0].name} was added to the database')          # final print statement


def moveoldfiles(newfiles):
    """
    This function moves GPX files to the past data folder once they are appended to the database
    :param newfiles: list of valid GPX filenames
    """

    curpath = r'C:\Users\Jasha\PycharmProjects\ewb-pr\new_data'
    destpath = r'C:\Users\Jasha\PycharmProjects\ewb-pr\gpx'
    for filename in newfiles:

        # old and new filepaths
        cur = os.path.join(curpath, filename)
        dest = os.path.join(destpath, filename)

        # move file and then remove from old directory
        shutil.move(cur, destpath)
        print(f'{cur} was fully distributed into the directory, and moved')


if __name__ == '__main__':

    # initial file loads
    files = loadgpxfiles()
    conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')

    append_names(conn, files)
    createcontours(conn, files)
    moveoldfiles(files)


