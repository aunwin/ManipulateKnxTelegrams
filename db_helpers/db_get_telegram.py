import mysql.connector
from db_helpers import db_update
from db_helpers import knxTelegram


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

    result_set = [knxTelegram.KnxTelegram]
    for row in cursor:
        temp = knxTelegram.KnxTelegram()
        temp.properties['sequence_number'] = row[0]
        temp.properties['timestamp'] = row[1]
        temp.properties['source_addr'] = row[2]
        temp.properties['destination_addr'] = row[3]
        temp.properties['apci'] = row[4]
        temp.properties['tpci'] = row[5]
        temp.properties['priority'] = row[6]
        temp.properties['repeated'] = row[7]
        temp.properties['hop_count'] = row[8]
        temp.properties['apdu'] = row[9]
        temp.properties['payload_length'] = row[10]
        temp.properties['cemi'] = row[11]
        temp.properties['is_manipulated'] = row[12]
        temp.properties['attack_type_id'] = row[13]

        result_set.append(temp)

    return result_set
