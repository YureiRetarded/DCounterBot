from betterconf import Config, field
import jsonprovider

provider = jsonprovider.JSONProvider()


class DCounterConfig(Config):
    token = field('DISCORD_TOKEN', default='none', provider=provider)


class DBConfig(Config):
    db_host = field('DB_HOST', default='localhost', provider=provider)
    db_user = field('DB_USER', default='root', provider=provider)
    db_password = field('DB_PASSWORD', default='12345678', provider=provider)
    db_name = field('DB_NAME', default='dcounter', provider=provider)
