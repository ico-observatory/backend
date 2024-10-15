"""
Django local settings for ICO project.
"""

import json

from ico.settings.base import *  # pylint: disable=W0614, W0401


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

try:
    with open('/etc/ico/config/production.json') as f:
        SETTINGS = json.loads(f.read())
except FileNotFoundError:
    SETTINGS = {}

DATABASES = {
    'default': {
        'ENGINE': get_env_var("DB_ENGINE", SETTINGS),
        'NAME': get_env_var("DB_NAME", SETTINGS),
        'USER': get_env_var("DB_USER", SETTINGS),
        'PASSWORD': get_env_var("DB_PASSWORD", SETTINGS),
        'HOST': get_env_var("DB_HOST", SETTINGS),
        'PORT': get_env_var("DB_PORT", SETTINGS)
    }
}
DOMAIN = get_env_var("DOMAIN", SETTINGS)
SECRET_KEY = get_env_var("SECRET_KEY", SETTINGS)

TIME_ZONE = 'America/Sao_Paulo'


# CRONJOBS = [
#     ('*/5 * * * *', 'ico.core.cron.reviews.notify_late_reviews', '>> ' + BASE_DIR + '/media/log/notify_late_reviews.log'),
#     ('*/5 * * * *', 'ico.core.cron.reviews.notify_remind_reviews', '>> ' + BASE_DIR + '/media/log/notify_remind_reviews.log'),
# ]
# CRONTAB_DJANGO_SETTINGS_MODULE = 'ico.settings.local'

# CRONTAB_COMMAND_SUFFIX = '2>&1'