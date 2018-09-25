import mysql.connector
from mysql.connector import errorcode

from config import dbconfig as db_cfg


def init_db_connections():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**db_cfg.src_db)
        cursor = connection.cursor()

        # get version of database
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()
        print(f'DB version: {db_version}')

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return connection, cursor


def close_db_connection(connection, cursor):
    # Clean up
    cursor.close()
    connection.close()
    return