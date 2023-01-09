from mysql.connector import connect, Error
import config

cfg = config.DBConfig()
try:
    with connect(
            host=cfg.db_host,
            user=cfg.db_user,
            password=cfg.db_password,
            database=cfg.db_name,
    ) as connection:
        print('Connect successfully')
        print(connection)
except Error as e:
    print('Connect error')
    print(e)
