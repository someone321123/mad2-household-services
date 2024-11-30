class Config():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True
    # cache specific
    CACHE_TYPE =  "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 30
    CACHE_REDIS_PORT = 6379