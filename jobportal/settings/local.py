from .base import *  # noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="DKWx_5S-4Bdr3bqsZe-QCTVobu04hD54J7zqcmPeR9_HySIqosk",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]
DOMAIN = env("DOMAIN")
SITE_NAME = "jobportal"
