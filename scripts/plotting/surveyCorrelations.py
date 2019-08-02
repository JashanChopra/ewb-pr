# library imports
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3

from databaseFuncs import get_conn


def pivotTables(conn):
    pass


if __name__ == '__main__':
    db = r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db'            # database location
    conn = get_conn(db)                                                         # get sqllite 3 connection
    pass
