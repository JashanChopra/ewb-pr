"""
This script is the central script to run for taking new data GPX files and adding them to the database. Documentation
for it can be found in the Puerto Rico Google Drive under the 2018-2019 --> Subteams --> Design folder
"""

# import libraries
from database.gpxfuncs import loadgpx, loadgpxfiles
from database.databaseFuncs import create_poi, get_conn, create_contour


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
                        waypoint.time)

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

        for track in gpx.tracks:                                                            # loop over each track
            for segment in track.segments:                                                  # loop over each segment
                for point in segment.points:                                                # loop over each point
                    addpoint = (point.latitude, point.longitude, point.elevation)           # create db entry
                    create_contour(conn, addpoint)                                          # add to db

        print(f'Each point of {len(gpx.tracks)} tracks was added to the database')          # final print statement


if __name__ == '__main__':

    # initial file loads
    files = loadgpxfiles()
    conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')

    append_names(conn, files)
    createcontours(conn, files)



