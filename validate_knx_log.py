#!/usr/bin/env python3

from db_helpers import db_acces as db
from config import dbconfig

connection, cursor = db.init_db_connections(dbconfig)

sql_statement = f'SELECT * FROM {dbconfig.knx_log_db["table"]} LIMIT 10;'

cursor.execute(sql_statement)

for row in cursor:
    print(row)

db.close_db_connection(connection, cursor)



