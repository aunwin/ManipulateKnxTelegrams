#!/usr/bin/env python3

from db_helpers import db_acces as db
from db_helpers import knxTelegram as knx_telegram
from db_helpers import db_update
from db_helpers import db_get_telegram
from config import dbconfig
import binascii
import baos_knx_parser as knx
import recalculate_cemi


def telegram_consistence_check(dbconfig, cursor):
    # todo turn statement into more generall statement (Filter)
    sql_statement = f'SELECT * FROM {dbconfig["table"]};'

    cursor.execute(sql_statement)

    inconsitent_sequence_numbers = []
    for row in cursor:
        dbTelegram = knx_telegram.KnxTelegram()
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
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'src-Property: dbValue = {dbTelegram.properties["source_addr"]} - '
                  f'parsedValue = {parsedTelegram.src}')
            propertie_deviations += 1

        if dbTelegram.properties["destination_addr"] != str(parsedTelegram.dest):
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'dest-Property: dbValue = {dbTelegram.properties["destination_addr"]} - '
                  f'parsedValue = {parsedTelegram.dest}')
            propertie_deviations += 1

        if dbTelegram.properties["apci"] != str(parsedTelegram.apci):
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'apci-Property: dbValue = {dbTelegram.properties["apci"]} - '
                  f'parsedValue = {parsedTelegram.apci}')
            propertie_deviations += 1

        if dbTelegram.properties["tpci"] != str(parsedTelegram.tpci):
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'tpci-Property: dbValue = {dbTelegram.properties["tpci"]} - '
                  f'parsedValue = {parsedTelegram.tpci}')
            propertie_deviations += 1

        if dbTelegram.properties["priority"] != str(parsedTelegram.priority):
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'priority-Property: dbValue = {dbTelegram.properties["priority"]} - '
                  f'parsedValue = {parsedTelegram.priority}')
            propertie_deviations += 1

        if dbTelegram.properties["repeated"] != parsedTelegram.repeat:
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'repeated-Property: dbValue = {dbTelegram.properties["repeated"]} - '
                  f'parsedValue = {parsedTelegram.repeat}')
            propertie_deviations += 1

        if dbTelegram.properties["hop_count"] != parsedTelegram.hop_count:
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'hop_count-Property: dbValue = {dbTelegram.properties["hop_count"]} - '
                  f'parsedValue = {parsedTelegram.hop_count}')
            propertie_deviations += 1

        if binascii.a2b_hex(dbTelegram.properties["apdu"]) != parsedTelegram.payload:
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'apdu-Property: dbValue = {dbTelegram.properties["apdu"]} - '
                  f'parsedValue = {parsedTelegram.payload}')
            propertie_deviations += 1

        if dbTelegram.properties["payload_length"] != parsedTelegram.payload_length:
            print(f'DEBUG: In Telegram with Sequence_Number = {dbTelegram.properties["sequence_number"]} '
                  f'payload_length-Property: dbValue = {dbTelegram.properties["payload_length"]} - '
                  f'parsedValue = {parsedTelegram.payload_length}')
            propertie_deviations += 1

        if propertie_deviations:
            print(f'WARNING: This telegram contains {propertie_deviations} property-missmatches')
            inconsitent_sequence_numbers.append(dbTelegram.properties['sequence_number'])
        # print(parsedTelegram.__dict__)
        # print(parsedTelegram)

    if len(inconsitent_sequence_numbers) > 0:
        print(f'WARNING: This set of telegrams contains {len(inconsitent_sequence_numbers)} invalid telegrams!')

    return inconsitent_sequence_numbers


# Setup
connection, cursor = db.init_db_connections(dbconfig.knx_attacks_log_db)


# Check and adapt db entries
inconsitent_telegrams = telegram_consistence_check(dbconfig.knx_attacks_log_db, cursor)

for seq_nbr in inconsitent_telegrams:
    telegram = db_get_telegram.get_db_telegram(dbconfig.knx_attacks_log_db, cursor, seq_nbr)[0] # select first entry of result set
    # todo clean this up - just writing all hop-count and src-address mistakes for now befor holiday break
    new_cemi_value = recalculate_cemi.set_hop_count(telegram.properties['hop_count'], telegram.properties['cemi'])
    new_cemi_value = recalculate_cemi.set_src_address(telegram.properties['source_addr'], new_cemi_value)
    db_update.update_db(dbconfig.knx_attacks_log_db, connection, cursor, seq_nbr, 'cemi',
                        new_cemi_value.decode('utf-8'))

inconsitent_telegrams = telegram_consistence_check(dbconfig.knx_attacks_log_db, cursor)
if len(inconsitent_telegrams) > 0:
    raise AssertionError('Still inconsistent db after updating')

# Teardown
db.close_db_connection(connection, cursor)
