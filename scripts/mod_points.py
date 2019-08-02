# import libraries
from gpxfuncs import loadgpx
from databaseFuncs import create_poi, get_conn, create_table

def append_names():
    """
    This script guides the user to change the names of points of interest and then updates the database, it takes
    no inputs. Run this python file to append names for any given script.
    """

    # ask the user to enter filename, repeat until correct
    while True:
        filename = input('Enter the filename of the GPX file you want to add to the database: ')
        try:
            gpx = loadgpx(filename)
            print(f'{filename} read properly')
            print('*------------*')
            break
        except FileNotFoundError as error:
            print(f'{filename} not found in directory, try again')
            pass

    for waypoint in gpx.waypoints:
        namechange = input(f'Do you want to change the name of waypoint {waypoint.name}? [y/n]: ')
        if namechange == 'y':
            waypoint.name = input('Enter the new name of the waypoint: ')
            print(f'The new name of this waypoint is {waypoint.name}')
        else:
            print(f'The waypoint name will stay as {waypoint.name}')

        addpoint = (waypoint.name, waypoint.latitude,
                    waypoint.longitude, waypoint.elevation,
                    waypoint.time)

        conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')
        idx = create_poi(conn, addpoint)
        print(f'{waypoint.name} has been added to the database with id {idx}')


if __name__ == '__main__':
    append_names()
