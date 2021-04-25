from os import environ as env
DATABASE_URI = f"postgresql://{env['user']}:{env['password'] }@{env['host']}:{env['port']}/{env['database']}"  # sqlAlchemy 1.4 - postgresql as driver

