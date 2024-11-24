import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    TITLE: str = "FastAPI Template"
    DESC: str = "FastAPI Template API"

    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001

    _db_dialect_and_driver = "mysql+mysqldb"
    DB_URL: str = "{}://{}:{}@{}:{}/{}".format(
        _db_dialect_and_driver,
        os.getenv("DB_USER"),
        os.getenv("MYSQL_ROOT_PASSWORD"),
        os.getenv("DB_LOCAL_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("MYSQL_DATABASE"),
    )
    
    ACCESS_TOKEN_EXPIRE_PERIOD: int = 10 * 60 * 60
    REFRESH_TOKEN_EXPIRE_PERIOD: int = 24 * 60 * 60

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"

    HASH_ID_SALT: str = os.getenv("HASH_ID_SALT")
    HASH_ID_MIN_LENGTH: str = os.getenv("HASH_ID_MIN_LENGTH")


class LocalConfig(Config):
    ...


class DevelopmentConfig(Config):
    DB_URL: str = "{}://{}:{}@{}:{}/{}".format(
        Config._db_dialect_and_driver,
        os.getenv("DB_USER"),
        os.getenv("MYSQL_ROOT_PASSWORD"),
        os.getenv("DB_DOCKER_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("MYSQL_DATABASE"),
    )


class TestConfig(Config):
    DB_URL: str = "sqlite:///test.db"


def get_config() -> Config:
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "test": TestConfig(),
    }
    return config_type[env]

config: Config = get_config()
