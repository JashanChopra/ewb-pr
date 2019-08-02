# import libraries
import gpxpy
import os
import gpxpy.gpx

# file dir
homedir = r'C:\Users\Jashan\PycharmProjects\ewb-pr'
rundir = os.path.join(homedir, 'gpx')
filename = input('Enter the filename of the GPX file you want to add to the database: ')
fileloc = os.path.join(rundir, filename)

# load gpx file
gpx_file = open(fileloc, 'r')
gpx = gpxpy.parse(gpx_file)

# # print all tracks (lat, long
# for track in gpx.tracks:
#     for segment in track.segments:
#         for point in segment.points:
#             print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

for waypoint in gpx.waypoints:
    namechange = input(f'Do you want to change the name of waypoint {waypoint.name}? [y/n]: ')
    if namechange == 'y':
        waypoint.name = input('Enter the new name of the waypoint: ')
        print(f'The new name of this waypoint is {waypoint.name}, it has been put in the DB')
    else:
        print(f'The waypoint name will stay as {waypoint.name}')

print('All waypoint names have been appended to the database for this file')

# for route in gpx.routes:
#     print('Route:')
#     for point in route.points:
#         print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

