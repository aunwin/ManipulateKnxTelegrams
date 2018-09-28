import mysql.connector
from db_helpers import db_update


def get_db_telegram(db_config, cursor, primary_key_value):
    # todo rewrite function to get list of primary_key_values to get possiblity to get more telegrams the same time
    primary_key = db_update.get_primary_key_of_table(db_config, cursor)
    table = db_config['table']

    stmt = f'SELECT * FROM {table} WHERE {primary_key} = {primary_key_value}'

    try:
        cursor.execute(stmt)
    except mysql.connector.Error as err:
        print(f'Error while getting entry from database: {err}')
        raise Exception('Error while getting entry from database: %s', err)

    result_set = []
    for row in cursor:
        result_set.append(row)

    return result_set
