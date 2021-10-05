import os
import json

with open(".config.json", encoding="UTF-8") as f:
    _CONFIG_JSON = json.load(f)


def get_db_url():
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    if db_name is None or db_user is None or db_password is None or db_host is None or db_port is None:
        raise Exception("Database credentials are not set")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_token():
    token = os.getenv('TOKEN')
    if token is None:
        raise Exception("Token is not set")

    return token


class JSONGetter(type):
    """
    Implements a custom metaclass used for accessing
    configuration data by simply accessing class attributes.
    It provides two levels of nested sections.

    `section` is high-level configuration section of JSON.

    `subsection` is second-level configuration section of JSON.

    Example Usage:
        # .config.json
        {
            "bot": {
                "prefix": "!",
                "token": "YOUR_TOKEN",
            },
            "databases": {
                "main": {
                    "db_name": "NAME"
                },
                "sub": {
                    "db_name": "NAME"
                }
            }
        }

        # constants.py
        class BotConfig(metaclass=JSONGetter):
            section = "bot"

            prefix: str
            token: str

        class MainDatabaseConfig(metaclass=JSONGetter):
            section = "databases"
            subsection = "main"

            db_name: str

        # Usage in code
        from constants import BotConfig
        def get_token():
            return BotConfig.token
    """

    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.subsection is not None:
                return _CONFIG_JSON[cls.section][cls.subsection][name]
            return _CONFIG_JSON[cls.section][name]
        except KeyError as e:
            dotted_path = '.'.join(
                (cls.section, cls.subsection, name)
                if cls.subsection is not None else (cls.section, name)
            )
            raise AttributeError(repr(name)) from e

        def __getitem__(cls, name):
            return cls.__getattr__(name)

        def __iter__(cls):
            for name in cls.__annotations__:
                yield name, getattr(cls, name)


class Bot(metaclass=JSONGetter):
    section = "bot"

    prefix: str
    debug: bool
