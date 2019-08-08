import os
import exifread
import datetime as dt
from databaseFuncs import get_conn, get_poi
import pandas as pd

def filelist_pics(directory):
    """
    This function lists files from the given directory, but seperates them by filetype for pics
    :param directory: the directory with photos
    :return: list for each file type
    """

    import os

    rawfiles, jpegfiles = [], []
    with os.scandir(directory) as files:
        for file in files:
            if '.ARW' in file.name:
                rawfiles.append(file.name)

    return rawfiles


def get_raw_data(filename):
    """
    Gets the raw exif data for the file and returns the data and filename
    :param filename:
    :return:
    """
    f = open(filename, 'rb')
    tags = exifread.process_file(f)
    date = str(tags['Image DateTime'])
    datetime = dt.datetime(int(date[:4]),
                           int(date[5:7]),
                           int(date[8:10]),
                           int(date[11:13]),
                           int(date[14:16]),
                           int(date[17:19]))

    imgdet = [f.name[45:], datetime]
    return imgdet


def conv_poi_dt(list):
    """
    Converts the datetimes of the points of interest into datetime64
    """

    datetimes = []
    for item in list:
        current = dt.datetime(int(item[:4]),
                              int(item[5:7]),
                              int(item[8:10]),
                              int(item[11:13]),
                              int(item[14:16]),
                              int(item[17:19]))
        datetimes.append(current)
    return datetimes


if __name__ == '__main__':
    direc = r'C:\Users\Jashan\Desktop\Puerto Rico Pictures'
    conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')
    raws = filelist_pics(direc)
    raws = [os.path.join(direc, x) for x in raws]

    colnames = ['id', 'name', 'lat', 'long', 'elevation', 'dates', 'trackname']
    points = get_poi(conn)
    points = pd.DataFrame(points)
    points.columns = colnames

    empty = pd.DataFrame()

    for file in raws:
        imgdata = get_raw_data(file)
        imgdata = pd.DataFrame(imgdata).transpose()
        imgdata.columns = ['filename', 'datetime']

        points['datetime'] = conv_poi_dt(points['dates'])

        match = pd.merge_asof(imgdata.sort_values('datetime'),
                              points.sort_values('datetime'),
                              by='datetime',
                              direction='nearest')
        empty = empty.append(match)

    finaloutput = [empty['filename'], empty['datetime'], match['id']]
    print(finaloutput)


