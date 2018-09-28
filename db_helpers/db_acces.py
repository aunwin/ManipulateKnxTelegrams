import mysql.connector
from mysql.connector import errorcode


def init_db_connections(db_config):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(host = db_config['host'],
                                             user = db_config['user'],
                                             password = db_config['passwd'],
                                             db = db_config['db'],
                                             raise_on_warnings = db_config['raise_on_warnings'])
        cursor = connection.cursor()

        # todo debug output
        # get version of database
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()
        # print(f'DB version: {db_version}')

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
