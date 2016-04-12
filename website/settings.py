"""
Django settings for website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser
from django_auth_ldap.config import LDAPSearch

config = ConfigParser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
config.read(os.path.join(BASE_DIR, 'opsadmin.cfg'))
DB_HOST = config.get('db','host')
DB_PORT = config.getint('db','port')
DB_USER = config.get('db','user')
DB_PASSWD   = config.get('db','passwd')
DB_DATABASE = config.get('db','database')
#LDAP Configure
LDAP_STATUS = config.get('ldap','ldap_status')
LDAP_HOST = config.get('ldap','ldap_host')
LDAP_BIND_DN = config.get('ldap','ldap_bind_dn')
LDAP_BIND_PASSWD =config.get('ldap','ldap_bind_passwd')
LDAP_BASE = config.get('ldap','ldap_base')

if LDAP_STATUS == '0':
        AUTH_USER_MODEL = 'UserManage.User'
if LDAP_STATUS == '1':
        AUTH_LDAP_CONNECTION_OPTIONS = {
                ldap.OPT_REFERRALS: 0
        }

        AUTHENTICATION_BACKENDS = (
                'django_auth_ldap.backend.LDAPBackend',
                'django.contrib.auth.backends.ModelBackend',
        )

        AUTH_LDAP_SERVER_URI = LDAP_HOST
        AUTH_LDAP_BIND_DN = LDAP_BIND_DN
        AUTH_LDAP_BIND_PASSWORD = LDAP_BIND_PASSWD
        AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_BASE,ldap.SCOPE_SUBTREE,"(&(objectClass=person)(sAMAccountName=%(user)s))")
       #(&(objectCategory=Person)(sAMAccountName=*))                                                                       

        AUTH_LDAP_USER_ATTR_MAP = {
                "first_name": "givenName",
                "last_name": "sn",
                "email": "mail"
        }

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '28ta%!1(r3z17!xq4nh6-5!u_s-v37z!f#0!zt)jy61zwp4)a9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False
#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_forms_bootstrap',
    'website',
    'UserManage',
    'Asset',
    'Authorize',
    'Audit',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'
WSGI_APPLICATION = 'website.wsgi.application'

SESSION_COOKIE_AGE=60*30
SESSION_EXPIRE_AT_BROWSER_CLOSE=True


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (
        MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
else:
    MYSQL_HOST = DB_HOST
    MYSQL_PORT = DB_PORT
    MYSQL_USER = DB_USER
    MYSQL_PASS = DB_PASSWD
    MYSQL_DB = DB_DATABASE

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : MYSQL_DB,
        'USER' : MYSQL_USER,
        'PASSWORD' : MYSQL_PASS,
        'HOST' : MYSQL_HOST,
        'PORT' : MYSQL_PORT,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

AUTH_USER_MODEL = 'UserManage.User'

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

#set TEMPLATE_DIRS
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

#TEMPLATE zh_CN
FILE_CHARSET='utf-8'
DEFAULT_CHARSET='utf-8'
