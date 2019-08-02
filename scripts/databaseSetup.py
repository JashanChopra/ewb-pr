"""
This script creates the database used to store GPS point of interest data
"""


import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    """
    Creates a connection to the database
    :param db_file: the name of the sqlite database file
    """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    dbloc = r'C:\Users\Jashan\PycharmProjects\ewb-pr\data'
    create_connection(os.path.join(dbloc, 'keypoints.db'))
    create_connection(os.path.join(dbloc, 'tracks.db'))
    print('Databases Created')

