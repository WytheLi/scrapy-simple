DEFAULT_LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
DEFAULT_LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOGGER_NAME = "scrapy_simple"

DEFAULT_SETTINGS = {
    "LOG_ENABLED": True,
    "LOG_ENCODING": "utf-8",
    "LOG_FILE": None,
    "LOG_FILE_APPEND": True,
    "LOG_FORMAT": DEFAULT_LOG_FORMAT,
    "LOG_DATEFORMAT": DEFAULT_LOG_DATEFORMAT,
    "LOG_LEVEL": DEFAULT_LOG_LEVEL,
    "LOG_SHORT_NAMES": True,
    "LOG_STDOUT": False,
    "LOG_NAME": DEFAULT_LOGGER_NAME,
}

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        DEFAULT_LOGGER_NAME: {"level": "DEBUG"},
        "requests": {"level": "WARNING"},
        "urllib3": {"level": "WARNING"},
    },
}
