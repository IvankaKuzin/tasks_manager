from tasks_manager.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ivxpeye&&_r30qpg4=)br)utmi^jmu#71)+itc#(ewy05_v@7_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}