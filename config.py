"""Configuration settings for the Flask application."""


import datetime
import os
from secrets import token_hex
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", token_hex(32))
    # JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", token_hex(32))
    # JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(weeks=4)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///financial.db"
    JWT_SECRET_KEY = "f97bdc26a066f6f100721f609022a3f57d1d9254f62ef55f6a0017c875c2459b"


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_financial.db"
    JWT_SECRET_KEY = "fba82ad33aab56ed623ad93f561bf234db8193231bf30af2770f7dabf762d497"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_PRIVATE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", token_hex(32))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", token_hex(32))


CONFIG = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(environment="default"):
    """Get configuration based on the specified environment."""

    return CONFIG[environment]
