from .base import *

import dj_database_url

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

LOGIN_REDIRECT_URL = '/management/auth/login/'

SECRET_KEY = 'jasdfnasdioufb'

ALLOWED_HOSTS = ['2g1nm7hxt4.execute-api.sa-east-1.amazonaws.com', 'tortasjackies.com']