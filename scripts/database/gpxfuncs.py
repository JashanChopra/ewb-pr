"""
This script contains general functions required for the manipulation of gpx funtions in python
"""

# import libraries
import gpxpy
import os
import gpxpy.gpx


def loadgpx(filename):
    """
    This function loads a gpx file from the gpx folder in this repo
    :param filename:
    :return: gpx file
    """

    # set directories
    homedir = r'C:\Users\Jashan\PycharmProjects\ewb-pr'
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

    newdatadir = r'C:\Users\Jashan\PycharmProjects\ewb-pr\new_data'
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

    # imports
    from math import radians, cos, sin, asin, sqrt

    # map to radians
    slat, slong, elat, elong = map(radians,
                                   [slat, slong, elat, elong])

    # haversine formula
    dlong = elong - slong
    dlat = elat - slat
    arc = (sin(dlat/2)**2) + (cos(slat)) * (cos(elat)) * (sin(dlong/2)**2)
    c = 2 * asin(sqrt(arc))
    r = 6371
    dist = c * r

    return dist


