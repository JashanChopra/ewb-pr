from gpxfuncs import loadgpx, haversine, loadgpxfiles
import pandas as pd
from databaseFuncs import get_conn, get_poi, get_track, get_track_names


def addtodb():
    """
    This function combines the two elevation values and then adds it to the db
    :param conn: a valid sqlite3 db connection
    :param df: dataframe of combined GPS and LIDAR data
    """

    # read final outputted csv
    clean = pd.read_csv('comb.csv', header=None)
    clean.columns = ['lat', 'long', 'elev_gps', 'time', 'time2', 'elev_lidar', 'dist']
    elev = []
    # combine elevations
    for i in list(range(len(clean))):
        # If the elevation difference is greater than one contour, use the LIDAR elevation
        if abs(clean['elev_lidar'].iloc[i] - clean['elev_gps'].iloc[i]) > 2:
            elev.append((clean['elev_lidar'].iloc[i] + clean['elev_gps'].iloc[i]) / 2)
        # Else, we use the average of the GPS elev and the lidar elev
        else:
            elev.append(clean['elev_lidar'].iloc[i])
    clean['elev'] = elev
    clean.drop(['elev_gps', 'elev_lidar', 'time2', 'dist'], axis=1, inplace=True)

    # output to csv
    clean.to_csv('final_poi.csv', mode='a', index=False)


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
                                                     'elev_cl'], axis=1)
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


def get_gps(files):

    points = get_poi(conn)
    alltracks = []
    for point in points:
        alltracks.append([point[1], point[2], point[3], point[4], point[5]])

    print('All points of interest have been plotted')
    # for filename in files:
    #     try:
    #         gpx = loadgpx(filename)
    #         print(f'{filename} read properly')
    #     except FileNotFoundError as error:
    #         print(f'{filename} not found in directory, try again')
    #         pass
    #
    #     # Apply gpxpy smoothing algorithms
    #     gpx.reduce_points(5000, min_distance=2)
    #     gpx.smooth(vertical=True, horizontal=True)
    #
    #     alltracks = []
    #     for track in gpx.tracks:                                                            # loop over each track
    #         for segment in track.segments:                                                  # loop over each segment
    #             for point in segment.points:                                                # loop over each point
    #                 # create point entry
    #                 addpoint = [gpx.tracks[0].name, point.latitude, point.longitude, point.elevation]
    #                 alltracks.append(addpoint)

    gpsDF = pd.DataFrame(alltracks)                                         # convert to dataframe
    gpsDF.columns = ['name', 'lat', 'long', 'elev', 'time']                 # rename columns

    print('GPS Dataframe Created')                                          # print statement
    return gpsDF


if __name__ == '__main__':
    dir = r'C:\Users\Jashan\PycharmProjects\ewb-pr\gpx\5ft contours.gpx'                    # directory of lidar data
    conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')            # create sqllite conn
    files = loadgpxfiles()

    # lidar = get_lidar(dir)                                                                  # get lidar data
    # lidar.to_csv('lidar.csv', index_label=False)                                            # save to csv
    # del(lidar)                                                                              # delete to conserve memory
    # print('LIDAR Data saved to CSV')                                                        # print statement

    gps = get_gps(files)                                                                     # get gps data

    reader = pd.read_csv('lidar.csv', chunksize=1000)                                       # read lidar data chunked
    tol = 0.0015                                                                              # kilometer tolerance
    [bulkprocess(gps, r, tol) for r in reader]                                              # merge operation on chunk

    addtodb()
