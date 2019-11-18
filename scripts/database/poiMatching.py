# Stu Smith provided our team with far superior LIDAR elevations -- these elevations are given in final_tracks_2.csv
# Unfortunately, he was unable to provide us with the elevation of our points of interest, thus this script will match
# the elevations to the points of interest!


import pandas as pd
import pathlib
from gpxfuncs import haversine


def bulkprocess(df, x):
    """
    This function performs a cross merge on two dataframes with latitude and longitude data, and then saves it to a csv file,
    it uses chunked pieces to conserve memory, and compares datapoints with the haversine difference
    :param df: the original GPS points to aqcuire matches for
    :param x: chunked versions to match with
    :param tolerance: number of kilometers in which matches should be saved
    """

    # perform a full cross merge with a false dropped key
    merged = pd.merge(df.assign(key=0),
                      x.assign(key=0),
                      on='key').drop('key', axis=1)
    print('Full Cross Merge Performed')

    # calculate the haversine difference between points to compare
    merged['dist'] = haversine(merged['lat_x'].tolist(), merged['long_x'].tolist(),
                               merged['lat_y'].tolist(), merged['long_y'].tolist())
    print('Haversine Distance Calculated')

    # find the closest match based on the haversine difference
    closest = merged.loc[merged.groupby(['id'])['dist'].idxmin()]
    print('Closest matches found')

    # merge the closest on the name with following suffixes, dropping old data
    dropcol = ['elev_x', 'name_y', 'time_y', 'dist', 'long_y', 'lat_y', 'elev_y','name_y']
    closest.drop(columns=dropcol, inplace=True)
    closest.columns = ['id', 'name', 'lat', 'long', 'time', 'closest track point', 'elev']

    return closest


def matchElev(poidir, trackdir):

    # load csv data
    poi = pd.read_csv(poidir)
    track = pd.read_csv(trackdir)

    # perform cross merge to combine points
    refined_poi = bulkprocess(poi, track)

    return refined_poi


if __name__ == "__main__":

    # get directories
    homedir = pathlib.PurePath(r'C:\Users\jasha\PycharmProjects\ewb-pr')
    datadir = homedir.joinpath('data')
    poidir = datadir.joinpath('keyPoints.csv')
    trackdir = datadir.joinpath('final_tracks_2.csv')

    # output POI with better elevation
    new = matchElev(poidir, trackdir)

    # save to .csv
    new.to_csv(r'C:\Users\jasha\PycharmProjects\ewb-pr\data\keyPoints2.csv')
