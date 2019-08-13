"""
This script contains multiple functions that pertain to modifying the sqllite3 databases
"""

import sqlite3
from sqlite3 import Error


def get_conn(db):
    """
    Create a database connection to the supplied database
    :param db: the database file path
    :return: the connection to the database
    """

    # try to get connection to sqlite3 database otherwise throw error
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

    return None


def create_poi(conn, point):
    """
    Creates a new point of interest in the database
    :param conn: the sql connection
    :param point: the point of interest, a tuple with the required fields. ex: (name, lat, long, elevation)
    :return: the last row id of the database
    """

    sql = ''' INSERT INTO poi(name, lat, long, elevation, time, trackname)                 
              VALUES(?,?,?,?,?, ?) '''                                              # sql insert statement
    cur = conn.cursor()                                                             # connection cursor
    cur.execute(sql, point)                                                         # execute sql
    # conn.commit()                                                                   # commit to db
    return cur.lastrowid                                                            # returns last row id
    cur.close()                                                                     # close db when finished


def create_contour(conn, point):
    """
    Creates a new point of interest in the database
    :param conn: the sql connection
    :param point: the point of interest, a tuple with the required fields. ex: (name, lat, long, elevation)
    :return: the last row id of the database
    """

    # this function is similar to the above create_poi()
    sql = ''' INSERT INTO contour(lat, long, elevation, trackname)
              VALUES(?,?,?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, point)
    conn.commit()
    return cur.lastrowid
    cur.close()


def create_table(conn, name, category=1):
    """
    Creates a table for the database with a valid conn
    :param conn: a valid DB sqlite3 connection
    :param name: the table name
    """

    if category == 1:
        # execute sql for creating a table with any name
        sql = f""" CREATE TABLE IF NOT EXISTS {name} (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            lat,                                
                                            long,
                                            elevation,
                                            time,
                                            trackname text NOT NULL
                                        ); """                      # table names should be reset by category
    elif category == 2:
        # execute sql for creating a table with any name
        sql = f""" CREATE TABLE IF NOT EXISTS {name} (
                                                id integer PRIMARY KEY,
                                                lat,                                
                                                long,
                                                elevation,
                                                trackname text NOT NULL
                                            ); """  # table names should be reset by category

    elif category == 3:
        # execute sql for creating a table with any name
        sql = f""" CREATE TABLE IF NOT EXISTS {name} (
                                                    id integer PRIMARY KEY,
                                                    lat,                                
                                                    long,
                                                    elevation,
                                                    trackname text NOT NULL
                                                    ); """  # table names should be reset by category

    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)


def get_poi(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM poi")
    allrows = cur.fetchall()

    return allrows


def get_track(conn):
    cur = conn.cursor()
    cur.execute("SELECT * from contour")
    allrows = cur.fetchall()

    return allrows


def get_track_names(tracks):
    """
    This function will seperate tracks by their name to avoid lines cutting across sections
    :param tracks: the list of each row from 'contours' table of the GPS database
    :return: list of lists, each secondfold list contains rows of contour with the given name
    """

    names = []
    for track in tracks:
        names.append(track[4])

    uniquenames = list(set(names))

    return uniquenames


if __name__ == '__main__':
    db = r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db'
    conn = get_conn(db)
    create_table(conn, 'cleaned', category=3)





