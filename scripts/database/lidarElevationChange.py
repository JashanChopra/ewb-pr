from gpxfuncs import loadgpx, haversine
import pandas as pd
from databaseFuncs import get_conn, get_poi, get_track, get_track_names

# Get LIDAR Data into an organized dataframe
dir = r'C:\Users\Jashan\PycharmProjects\ewb-pr\gpx\5ft contours.gpx'
lidar = loadgpx(dir)

allpoints = []
for track in lidar.tracks:
    for segment in track.segments:
        for point in segment.points:
            allpoints.append([point.latitude, point.longitude, point.elevation])

lidarDF = pd.DataFrame(allpoints)
lidarDF.columns = ['latitude', 'longitude', 'elevation']
print('LIDAR Dataframe Created')

# Get the track data
conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')
tracks = get_track(conn)

alltracks = []
for track in tracks:
    alltracks.append([track[0], track[1], track[2], track[3]])

gpsDF = pd.DataFrame(alltracks)
gpsDF.columns = ['name', 'lat', 'long', 'elev']

print('GPS Dataframe Created')

# Merge via cross join on false key
alldata = pd.merge(gpsDF.assign(key=0),
                   lidarDF.assign(key=0),
                   on='key').drop('key', axis=1)

# create a distance column
alldata['dist'] = haversine(alldata['lat'], alldata['long'],
                            alldata['latitude'], alldata['longitude'])

# identify close proximity matches
closest = alldata.loc[alldata.groupby(['name'])['dist'].idxmin()]

# merge back with original dataframe
data_locs = gpsDF.merge(closest, on=['name'],
                        suffixes=('', '_cl')).drop(['latitude', 'longitude'], axis=1)

print('Data sets have been merged')


