"""
This script contains general functions required for the manipulation of gpx funtions in python
"""

# import libraries
import gpxpy
import os
import gpxpy.gpx
import numpy as np
from convToRadians import conv
import pandas as pd
import shutil


def loadgpx(filename):
    """
    This function loads a gpx file from the gpx folder in this repo
    :param filename:
    :return: gpx file
    """

    # set directories
    homedir = r'C:\Users\Jasha\PycharmProjects\ewb-pr'
    rundir = os.path.join(homedir, 'gpx')
    fileloc = os.path.join(rundir, filename)

    # load gpx file
    gpx_file = open(fileloc, 'r')
    gpx = gpxpy.parse(gpx_file)

    # return gpx file
    return gpx


def loadgpxfiles():
    """
    This function loads all GPX files from the new_data folder to avoid having to manually enter datafile names
    :return: a list of all the GPX file names in the directory
    """
    # import statements
    import os

    newdatadir = r'C:\Users\Jasha\PycharmProjects\ewb-pr\new_data'
    filenames = []
    for filename in os.listdir(newdatadir):
        if filename.endswith('gpx'):
            gpxfilepath = os.path.join(newdatadir, filename)
            filenames.append(gpxfilepath)

    return filenames


def haversine(slat, slong, elat, elong):
    """
    This function uses the haversine formula calculate the distance between
    two GPS points
    :return: distance
    """

    # map to radians and convert to numpy array
    slat = conv(slat)
    slong = conv(slong)
    elat = conv(elat)
    elong = conv(elong)

    # haversine formula
    d = np.sin((elat - slat)/2)**2 + np.cos(slat) * np.cos(elat) * np.sin((elong - slong)/2)**2
    arc = np.arcsin(np.sqrt(d))
    r = 6372.8
    dist = 2 * r * arc

    return dist


def createcontours(newfiles):
    """
    This function creates a database entry for each point of each track of a GPX file
    :param newfiles: a list of valid gpx filenames in the given directory
    :param conn: an sqlite3 connection to the database
    :return:
    """
    contours = []
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
                    addpoint = [gpx.tracks[0].name, point.latitude, point.longitude,
                                point.elevation, point.time]                                # create db entry
                    contours.append(addpoint)

        print(f'Each point of {gpx.tracks[0].name} was added to the dataframe')             # final print statement

    contour = pd.DataFrame(contours, columns=['name', 'latitude', 'longitude', 'elevation', 'time'])
    return contour


def createpoi(newfiles):
    """
    This script guides the user to change the names of points of interest and then updates the database, it takes
    no inputs. Run this python file to append names for any given script.
    :param conn: a valid sqlite3 connection
    :param newfiles: a list of valid gpx filenames
    """

    # ask the user to enter filename, repeat until correct

    pois = []
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

            addpoint = [waypoint.name, waypoint.latitude,
                        waypoint.longitude, waypoint.elevation,
                        waypoint.time, gpx.tracks[0].name]
            pois.append(addpoint)

            print(f'{waypoint.name} has been added to dataframe')

    poi = pd.DataFrame(pois, columns=['name', 'latitude', 'longitude', 'elevation', 'time', 'track_name'])
    return poi


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


def get_track_names(tracks):
    """
    This function will seperate tracks by their name to avoid lines cutting across sections
    :param tracks: the list of each row from 'contours' table of the GPS database
    :return: list of lists, each secondfold list contains rows of contour with the given name
    """

    names = []
    for index, track in tracks.iterrows():
        names.append(track[1])

    uniquenames = list(set(names))

    return uniquenames


def createcontours_smooth(newfiles):
    """
    This function creates a database entry for each point of each track of a GPX file
    :param newfiles: a list of valid gpx filenames in the given directory
    :param conn: an sqlite3 connection to the database
    :return:
    """
    contours = []
    for filename in newfiles:
        try:
            gpx = loadgpx(filename)
            print(f'{filename} read properly')
            print('*------------*')
        except FileNotFoundError as error:
            print(f'{filename} not found in directory, try again')
            pass

        #  Apply gpxpy smoothing algorithms
        gpx.reduce_points(1000, min_distance=2)
        gpx.smooth(vertical=True, horizontal=True)
        gpx.smooth(vertical=True, horizontal=True)

        print('Adding each point in track, this may take a moment')
        for track in gpx.tracks:                                                            # loop over each track
            for segment in track.segments:                                                  # loop over each segment
                for point in segment.points:                                                # loop over each point
                    addpoint = [gpx.tracks[0].name, point.latitude, point.longitude,
                                point.elevation, point.time]                                # create db entry
                    contours.append(addpoint)

        print(f'Each point of {gpx.tracks[0].name} was added to the dataframe')             # final print statement

    contour = pd.DataFrame(contours, columns=['name', 'latitude', 'longitude', 'elevation', 'time'])
    return contour


