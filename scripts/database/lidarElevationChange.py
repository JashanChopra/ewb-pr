from gpxfuncs import loadgpx, haversine
import pandas as pd
from databaseFuncs import get_conn, get_poi, get_track, get_track_names


def bulkprocess(df, x, tolerance):
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
    merged['dist'] = haversine(merged['lat'].tolist(), merged['long'].tolist(),
                               merged['latitude'].tolist(), merged['longitude'].tolist())
    print('Haversine Distance Calculated')

    # find the closest match based on the haversine difference
    closest = merged.loc[merged.groupby(['name'])['dist'].idxmin()]
    closest = closest[closest['dist'] < tolerance]                          # remove values if distance is poor match
    print('Closest matches found')

    # merge the closest on the name with following suffixes, dropping old data
    data_locs = df.merge(closest, on=['name'],
                         suffixes=('', '_cl')).drop(['latitude', 'longitude',
                                                     'lat_cl', 'long_cl',
                                                     'elev_cl', 'name'], axis=1)
    # save to a csv file with addition
    data_locs.to_csv('comb.csv', mode='a', header=False, index=False)
    print('Single LIDAR merge performmed')


def get_lidar(dir):
    lidar = loadgpx(dir)                                                                # load gpx data
    print('LIDAR Data Loaded')                                                          # print statement

    allpoints = []                                                                      # preallocate list
    for track in lidar.tracks:                                                          # loop each track
        for segment in track.segments:                                                  # loop each segment
            for point in segment.points:                                                # loop each point
                allpoints.append([point.latitude, point.longitude, point.elevation])    # append details

    lidarDF = pd.DataFrame(allpoints)                                                   # create dataframe
    lidarDF.columns = ['latitude', 'longitude', 'elevation']                            # rename columns
    print('LIDAR Dataframe Created')

    return lidarDF


def get_gps(conn):

    tracks = get_track(conn)                                                # get each track in sql database

    alltracks = []                                                          # preallocate list
    for track in tracks:                                                    # loop throuhg each track
        alltracks.append([track[0], track[1], track[2], track[3]])          # append name, lat, long, elev

    gpsDF = pd.DataFrame(alltracks)                                         # convert to dataframe
    gpsDF.columns = ['name', 'lat', 'long', 'elev']                         # rename columns

    print('GPS Dataframe Created')                                          # print statement
    return gpsDF


if __name__ == '__main__':
    dir = r'C:\Users\Jashan\PycharmProjects\ewb-pr\gpx\5ft contours.gpx'                    # directory of lidar data
    conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')            # create sqllite conn

    lidar = get_lidar(dir)                                                                  # get lidar data
    lidar.to_csv('lidar.csv', index_label=False)                                            # save to csv
    del(lidar)                                                                              # delete to conserve memory
    print('LIDAR Data saved to CSV')                                                        # print statement

    gps = get_gps(conn)                                                                     # get gps data

    reader = pd.read_csv('lidar.csv', chunksize=1000)                                       # read lidar data chunked
    tol = 0.0015                                                                              # kilometer tolerance
    [bulkprocess(gps, r, tol) for r in reader]                                              # merge operation on chunk



    # Nick: "Im not saying Shrek Musical was a good musical, but I just went home and cried after it."
