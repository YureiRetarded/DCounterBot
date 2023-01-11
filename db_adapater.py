from mysql.connector import connect, Error
import config

cfg = config.DBConfig()


def db_select_one(query):
    try:
        with connect(
                host=cfg.db_host,
                user=cfg.db_user,
                password=cfg.db_password,
                database=cfg.db_name,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                if len(result) > 0:
                    return result
                else:
                    return None
    except Error as e:
        print('Connect error')
        print(e)


def db_create(query):
    try:
        with connect(
                host=cfg.db_host,
                user=cfg.db_user,
                password=cfg.db_password,
                database=cfg.db_name,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()

    except Error as e:
        print('Connect error')
        print(e)


def get_server(server_id):
    query = 'SELECT id,discord_server_id FROM servers WHERE discord_server_id=' + str(server_id)
    return db_select_one(query)


def create_server(discord_server_id):
    query = 'INSERT INTO servers (discord_server_id) VALUES (' + str(discord_server_id) + ')'
    return db_create(query)


def get_user(server_id, user_id):
    query = '''SELECT users.id, users.discord_user_id, users.server_id
     FROM dcounter.users
      LEFT JOIN (servers)
       ON (servers.id=users.server_id)
        WHERE servers.discord_server_id=''' + str(server_id) + ' AND users.discord_user_id=' + str(user_id)
    return db_select_one(query)


def addUser(server_id, user_id):
    query = 'INSERT INTO users (discord_user_id,server_id) VALUES (' + str(user_id) + ',' + str(server_id) + ')'
    return db_create(query)


def update_members_guild(server_id, members):
    server = get_server(server_id)[0]
    if server != None:
        for person in members:
            if get_user(server[1], person.id) == None:
                addUser(server[0], person.id)


def get_nomination(server_id):
    query = 'SELECT id,name,server_id FROM nominations WHERE server_id=' + str(server_id)
    return db_select_one(query)


def hasNomination(server_id):
    query = 'SELECT * FROM nominations WHERE server_id=' + str(server_id)
    return db_select_one(query)


def create_nomination(server_id, name):
    if hasNomination(server_id) == None:
        if len(name) > 30 and len(name) < 3:
            return [False, 'Слишком длинное название!']
        query = 'INSERT INTO nominations (server_id,name) VALUES (' + str(server_id) + ",'" + str(name) + "')"
        return db_create(query)
    else:
        return [False, 'Номинация уже есть!']


def add_user_to_nominate(nom_id, user_id):
    query = 'INSERT INTO nomination_user (nomination_id,user_id) VALUES (' + str(nom_id) + ',' + str(user_id) + ')'
    return db_create(query)


def get_user_nominate(user_id, nom_id):
    query = 'SELECT nomination_id,user_id,count FROM nomination_user WHERE nomination_id=' + str(
        nom_id) + ' AND user_id=' + str(user_id)
    return db_select_one(query)


# def add_users_to_nomination(server_id, members):
#     server = get_server(server_id)
#     nom = get_nomination(server[0])
#     for person in members:
#         if get_user(server[1], person.id) != None:
#             addUser(server[0], person.id)
#

def get_nomination_users(nomination_id):
    query = 'SELECT nomination_id,user_id,count FROM nomination_user WHERE nomination_id=' + str(nomination_id)
    return db_select_one(query)


def get_user_nominations(user_id, server_id):
    query = '''SELECT servers.discord_server_id, users.discord_user_id, nominations.name, nomination_user.count
     FROM nomination_user
      LEFT JOIN(servers,nominations,users) ON (nominations.server_id=servers.id AND nomination_user.nomination_id=nominations.id AND nomination_user.user_id=users.id)
       WHERE servers.discord_server_id=''' + str(server_id) + ' AND users.discord_user_id=' + str(user_id)
    return db_select_one(query)
