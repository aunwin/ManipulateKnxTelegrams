#!/usr/bin/env python3

from db_helpers import db_acces as db
from db_helpers import knxTelegram as dbKnxTelegram
from config import dbconfig
import binascii
import baos_knx_parser as knx
import update_cemi


def telegram_consistence_check(dbconfig, cursor):
    # todo turn statement into more generall statement (Filter)
    sql_statement = f'SELECT * FROM {dbconfig.knx_log_db["table"]};'

    cursor.execute(sql_statement)

    inconsitent_sequence_numbers = []
    for row in cursor:
        dbTelegram = dbKnxTelegram.KnxTelegram
        i = 0
        for dbItem in dbTelegram.properties:
            dbTelegram.properties[dbItem] = row[i]
            i += 1

        # todo debug output
        # for dbItem in dbTelegram.properties:
        #    print(str(dbItem) + ": " + str(dbTelegram.properties[dbItem]))

        parsedTelegram = knx.parse_knx_telegram(binascii.a2b_hex(dbTelegram.properties['cemi']))

        propertie_deviations = 0

        if dbTelegram.properties["source_addr"] != str(parsedTelegram.src):
            print(f'Error in src-Property: dbValue: {dbTelegram.properties["source_addr"]} - '
                  f'parsedValue: {parsedTelegram.src}')
            propertie_deviations += 1

        if dbTelegram.properties["destination_addr"] != str(parsedTelegram.dest):
            print(f'Error in dest-Property: dbValue: {dbTelegram.properties["destination_addr"]} - '
                  f'parsedValue: {parsedTelegram.dest}')
            propertie_deviations += 1

        if dbTelegram.properties["apci"] != str(parsedTelegram.apci):
            print(f'Error in apci-Property: dbValue: {dbTelegram.properties["apci"]} - '
                  f'parsedValue: {parsedTelegram.apci}')
            propertie_deviations += 1

        if dbTelegram.properties["tpci"] != str(parsedTelegram.tpci):
            print(f'Error in tpci-Property: dbValue: {dbTelegram.properties["tpci"]} - '
                  f'parsedValue: {parsedTelegram.tpci}')
            propertie_deviations += 1

        if dbTelegram.properties["priority"] != str(parsedTelegram.priority):
            print(f'Error in priority-Property: dbValue: {dbTelegram.properties["priority"]} - '
                  f'parsedValue: {parsedTelegram.priority}')
            propertie_deviations += 1

        if dbTelegram.properties["repeated"] != parsedTelegram.repeat:
            print(f'Error in repeated-Property: dbValue: {dbTelegram.properties["repeated"]} - '
                  f'parsedValue: {parsedTelegram.repeat}')
            propertie_deviations += 1

        if dbTelegram.properties["hop_count"] != parsedTelegram.hop_count:
            print(f'Error in hop_count-Property: dbValue: {dbTelegram.properties["hop_count"]} - '
                  f'parsedValue: {parsedTelegram.hop_count}')
            propertie_deviations += 1

        if binascii.a2b_hex(dbTelegram.properties["apdu"]) != parsedTelegram.payload:
            print(f'Error in apdu-Property: dbValue: {dbTelegram.properties["apdu"]} - '
                  f'parsedValue: {parsedTelegram.payload}')
            propertie_deviations += 1

        if dbTelegram.properties["payload_length"] != parsedTelegram.payload_length:
            print(f'Error in payload_length-Property: dbValue: {dbTelegram.properties["payload_length"]} - '
                  f'parsedValue: {parsedTelegram.payload_length}')
            propertie_deviations += 1

        if propertie_deviations:
            print(f'WARNING: This telegram contains {propertie_deviations} property-missmatches')
            inconsitent_sequence_numbers.append(dbTelegram.properties['sequence_number'])
        # print(parsedTelegram.__dict__)
        # print(parsedTelegram)

    if len(inconsitent_sequence_numbers) > 0:
        print(f'WARNING: This set of telegrams contains {len(inconsitent_sequence_numbers)} invalid telegrams!')

    return inconsitent_sequence_numbers

connection, cursor = db.init_db_connections(dbconfig)
inconsitent_telegrams = telegram_consistence_check(dbconfig, cursor)
print(len(inconsitent_telegrams))
#new_cemi = update_cemi.set_hop_count(5, dbTelegram.properties['cemi'])
#dbTelegram.properties['cemi'] = new_cemi

db.close_db_connection(connection, cursor)
