# This script was the initial script for transferring data from GPX form from the GPS itself into .csv files.

from gpxfuncs import loadgpxfiles, moveoldfiles, createpoi, createcontours


if __name__ == '__main__':

    # initial file loads
    newfiles = loadgpxfiles()

    # create contours
    contour = createcontours(newfiles)
    contour.to_csv(r'C:\Users\jasha\PycharmProjects\ewb-pr\finalized_data\rawTracks.csv')

    # create poi
    poi = createpoi(newfiles)
    poi.to_csv(r'C:\Users\jasha\PycharmProjects\ewb-pr\finalized_data\rawPoi.csv')

    moveoldfiles(newfiles)

