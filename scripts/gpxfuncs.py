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
