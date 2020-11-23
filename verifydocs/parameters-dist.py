# Database config
PG_ENGINE = 'django.db.backends.postgresql_psycopg2'
PG_DBNAME = 'vdc'
PG_DBUSER = ''
PG_DBPASSWORD = ''
PG_DBHOST = ''
PG_DBPORT = '5432'

# Project config
# $ openssl rand -base64 32
DJ_SECRET_KEY = ''
DJ_DEBUG = False
DJ_ALLOWED_HOSTS = ['*']
DJ_LANGUAGE_CODE = 'es-co'
DJ_TIME_ZONE = 'America/Bogota'
DJ_USE_I18N = False
DJ_USE_L10N = True
DJ_USE_TZ = False
DJ_SITE_ID = 1

DJ_URL_PROJECT = ''

CACHE_REDIS_HOST = ''
CACHE_REDIS_PORT = '6379'
CACHE_REDIS_DB = '1'

NAME_URL_FILE_QR = ''

WEB_CLIENT_URL = 'https://verifydocs.ufps.edu.co/'

#
# Email
#
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'