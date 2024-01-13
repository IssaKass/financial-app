"""Configuration settings for the Flask application."""


import datetime


class Config:
    """Base configuration class."""

    # pylint: disable=too-few-public-methods
    SECRET_KEY = "de641bd49626e8951d21f788"

    SQLALCHEMY_DATABASE_URI = "sqlite:///financial.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "3b6e5e0a75e8581f92110b7f"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(weeks=4)


class DevelopmentConfig(Config):
    """Development confiugration class."""

    # pylint: disable=too-few-public-methods
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration class."""

    # pylint: disable=too-few-public-methods
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_financial.db"


class ProductionConfig(Config):
    """Production confiugration class."""

    # pylint: disable=too-few-public-methods
    DEBUG = False

    SECRET_KEY = "3eaace33b55b8c04ed135319c7c839c7c5935490f4dff183e1dde4dde46353b6"

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://IssaKass:issakass2002@localhost:5432/financial"
    )

    JWT_SECRET_KEY = "403076f90595eca8c0ed389bc51022d11a7f881ccb495958012a96cf6801cb72"


CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(environment="default"):
    """Get configuration based on the specified environment."""

    return CONFIG[environment]
