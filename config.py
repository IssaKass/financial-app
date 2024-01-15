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
    SECRET_KEY = "1784226bc0e01c0b47699430b5fc62e3800b2336b7d852e17e20bf40da353673"
    JWT_SECRET_KEY = "b2a3f61c61cd81baafb9d1a12bb61e4e9c594d043206ce938ef840a3884d9e19"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///financial.db"


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_financial.db"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
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
