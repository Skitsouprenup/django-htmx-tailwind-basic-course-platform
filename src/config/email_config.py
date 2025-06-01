from decouple import config

env_vars = {
    "EMAIL_HOST_USER": config("EMAIL_HOST_USER", cast=str, default=None),
    "EMAIL_HOST_PASSWORD": config("EMAIL_HOST_PASSWORD", cast=str, default=None),
}

def get_email_env(key):

    if key in env_vars:
        return env_vars[key]
    return None

