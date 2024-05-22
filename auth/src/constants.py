import os

ENV = os.environ.get("ENV", "dev")
APP_VERSION = "1.0.0"
APP_PREFIX = "AUTH API"
APP_NAME = "AUTH API"
APP_DESCRIPTION = "API для авторизации"
APP_API_DOCS_TITLE = f"{APP_NAME} ({ENV.upper()})" if ENV != "dev" else APP_NAME

DEFAULT_ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
