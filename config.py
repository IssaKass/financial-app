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
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", token_hex(32))
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(weeks=4)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", "sqlite:///financial.db")
    JWT_SECRET_KEY = os.getenv("DEV_JWT_SECRET_KEY", token_hex(32))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL", "sqlite:///test_financial.db"
    )
    JWT_SECRET_KEY = os.getenv("TEST_JWT_SECRET_KEY", token_hex(32))


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_PRIVATE_URL",
        "postgresql://postgres:4C--EAgGcGFE134C5GefFg6bD3f3f3Dc@roundhouse.proxy.rlwy.net:32076/railway",
    )
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
    )
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", token_hex(32))


CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(environment="default"):
    """Get configuration based on the specified environment."""

    return CONFIG[environment]
