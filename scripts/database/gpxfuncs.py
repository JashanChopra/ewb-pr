"""
This script contains general functions required for the manipulation of gpx funtions in python
"""

# import libraries
import gpxpy
import os
import gpxpy.gpx
import numpy as np
from convToRadians import conv


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


