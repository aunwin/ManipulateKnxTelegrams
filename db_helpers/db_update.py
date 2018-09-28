import mysql.connector


def get_primary_key_of_table(db_config, cursor):
    table = db_config['table']

    stmt = f'SELECT k.COLUMN_NAME ' \
           f'FROM information_schema.table_constraints t ' \
           f'LEFT JOIN information_schema.key_column_usage k ' \
           f'USING(constraint_name,table_schema,table_name) ' \
           f'WHERE t.constraint_type="PRIMARY KEY" ' \
           f'AND t.table_schema=DATABASE() ' \
           f'AND t.table_name="{table}";'

    try:
        cursor.execute(stmt)
        result = []
        for row in cursor:
            result.append(row[0])
        if len(result) < 1:
            raise LookupError('No primary key found!')
        elif len(result) > 1:
            raise LookupError('Multiple primary keys found!')

        primary_key = result[0]
    except mysql.connector.Error as err:
        print(f'Error in get_primary_key_of_table:{err}')

    return primary_key
