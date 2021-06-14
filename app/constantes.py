from warnings import warn

SECRET_KEY = "i am a secret"
API_ROUTE = "/api"

if SECRET_KEY == "i am a secret":
    warn("The default secret has not been changed, you should do it", Warning)


class _TEST:
    SECRET_KEY = SECRET_KEY


class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    SECRET_KEY = "Iamasecret"

CONFIG = {"test": _TEST, "production": _PRODUCTION}