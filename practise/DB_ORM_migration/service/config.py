from os import environ as env

CONNECTION_VAGRANT_DB_SHOP = {
    'host': env['host'],
    'port': env['port'],
    'database': env['database'],
    'user': env['user'],
    'password': env['password']
}


