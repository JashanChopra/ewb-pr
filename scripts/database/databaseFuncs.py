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

    sql = ''' INSERT INTO poi(name, lat, long, elevation, time)                 
              VALUES(?,?,?,?,?) '''                                                 # sql insert statement
    cur = conn.cursor()                                                             # connection cursor
    cur.execute(sql, point)                                                         # execute sql
    conn.commit()                                                                   # commit to db
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
    sql = ''' INSERT INTO contour(lat, long, elevation)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, point)
    conn.commit()
    return cur.lastrowid
    cur.close()


def create_table(conn, name):
    """
    Creates a table for the database with a valid conn
    :param conn: a valid DB sqlite3 connection
    :param name: the table name
    """

    # execute sql for creating a table with any name
    sql = f""" CREATE TABLE IF NOT EXISTS {name} (
                                        id integer PRIMARY KEY,
                                        lat,                                
                                        long,
                                        elevation
                                    ); """                      # tablle names should be reset as required
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)


if __name__ == '__main__':
    db = r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db'
    conn = get_conn(db)
    # create_table(conn, 'contour')





