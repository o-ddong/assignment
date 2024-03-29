import json
import os
import pymysql

from .base import *

pymysql.install_as_MySQLdb()

with open(os.path.dirname(BASE_DIR)+'/.envs/.prd/.django.json', 'r') as django_env_file:
    django_envs = json.load(django_env_file)

with open(os.path.dirname(BASE_DIR)+'/.envs/.prd/.mysql.json', 'r') as mysql_env_file:
    mysql_envs = json.load(mysql_env_file)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': mysql_envs['MYSQL_DB'],
        'USER': mysql_envs['MYSQL_USER'],
        'PASSWORD': mysql_envs['MYSQL_PASSWORD'],
        'HOST': mysql_envs["MYSQL_HOST"],
        'PORT': mysql_envs["MYSQL_PORT"],
        'TIME_ZONE': 'Asia/Seoul',
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = django_envs['SECRET_KEY']

IV = django_envs['IV']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

WSGI_APPLICATION = 'config.wsgi.deploy.application'
