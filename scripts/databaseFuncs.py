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
              VALUES(?,?,?,?,?) '''
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

    sql = """ CREATE TABLE IF NOT EXISTS {name} (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)





