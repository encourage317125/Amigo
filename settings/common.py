# -*- coding: utf-8 -*-
'''Django settings for Amigo project.

see: https://docs.djangoproject.com/en/dev/ref/settings/
'''
# Standard Library
from os.path import dirname, join

# Third Party Stuff
import environ
from configurations import Configuration

# Build paths inside the project like this: os.path.join(ROOT_DIR, ...)
ROOT_DIR = dirname(dirname(__file__))
APP_DIR = join(ROOT_DIR, 'amigo')

env = environ.Env()


# Common Configurations
# ========================================================================
class Common(Configuration):
    # APP CONFIGURATION
    # -----------------
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django_sites',  # http://niwibe.github.io/django-sites/
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'grappelli',
        'django.contrib.admin',

        'amigo.base',
        'amigo.users',
        'amigo.events',
        'amigo.pages',
        'amigo.notifications',
        'tz_detect',

        'django_extensions',  # http://django-extensions.readthedocs.org/
        'rest_framework',  # http://www.django-rest-framework.org/
        'django_twilio_sms',  # https://github.com/nigma/django-twilio-sms
        'zeropush',  # https://github.com/hakanw/django-zeropush
        'versatileimagefield',  # https://github.com/WGBH/django-versatileimagefield/
        'corsheaders',  # https://github.com/ottoyiu/django-cors-headers
        'airbrake',  # https://github.com/airbrake/airbrake-django
    )

    # MIDDLEWARE CONFIGURATION
    # Note: Order in which they are added are important
    MIDDLEWARE_CLASSES = (
        # Make sure djangosecure.middleware.SecurityMiddleware is the first
        # middleware class listed
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'tz_detect.middleware.TimezoneMiddleware',
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    # Defaults to false, which is safe, enable them only in development.
    DEBUG = env.bool('DJANGO_DEBUG', default=False)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG

    # See:
    # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    FIXTURE_DIRS = (
        join(APP_DIR, 'fixtures'),
    )

    # MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        ('Amigo Admin', 'info@amigo.io'),
        ('Paul Zabelin', 'paul@amigo.io'),
        ('Dmitri Zdorov', 'dmitri@amigo.io'),
        ('Wei Ye', 'wei@amigo.io'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS
    # END MANAGER CONFIGURATION

    # EMAIL CONFIGURATION
    EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                        default='django.core.mail.backends.smtp.EmailBackend')

    # END EMAIL CONFIGURATION

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # In a Windows environment this must be set to your system time zone.
    TIME_ZONE = 'UTC'

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = 'en-us'

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = True

    # If you set this to False, Django will not format dates, numbers and
    # calendars according to the current locale.
    USE_L10N = True

    # If you set this to False, Django will not use timezone-aware datetimes.
    USE_TZ = True

    # TEMPLATE CONFIGURATION
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # Your stuff: custom template context processers go here
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        join(APP_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    # STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(ROOT_DIR, '.staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See:
    # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
    )

    # List of finder classes that know how to find static files in
    # various locations.
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    # END STATIC FILE CONFIGURATION

    # MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(ROOT_DIR, '.media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    # END MEDIA CONFIGURATION

    # URL Configuration
    ROOT_URLCONF = 'amigo.urls'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'wsgi.application'
    # End URL Configuration

    # AUTHENTICATION CONFIGURATION (only for django admin)
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
    )

    # CORS CONFIG
    CORS_ORIGIN_ALLOW_ALL = True

    # SLUGLIFIER
    AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
    # END SLUGLIFIER

    # LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'complete': {
                'format': '%(levelname)s:%(asctime)s:%(module)s %(message)s'
            },
            'simple': {
                'format': '%(levelname)s:%(asctime)s: %(message)s'
            },
            'null': {
                'format': '%(message)s',
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['null'],
                'propagate': True,
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    # DATABASE CONFIGURATION
    # ------------------------------------------------------------------------------
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = {
        'default': env.db("DATABASE_URL", default="postgres://localhost/amigo"),
    }
    DATABASES['default']['ATOMIC_REQUESTS'] = True
    DATABASES['default']['CONN_MAX_AGE'] = 60

    SITES = {
        "local": {"domain": "localhost:8000", "scheme": "http", "name": "localhost"},
        "remote": {
            "domain": env('SITE_DOMAIN', default=''),
            "scheme": env('SITE_SCHEME', default='https'),
            "name": env('SITE_NAME', default='Amigo'),
        },
    }

    SITE_ID = "remote"

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'amigo.base.api.pagination.PageNumberPagination',
        'PAGE_SIZE': 30,

        # 'Accept' header based versioning
        # http://www.django-rest-framework.org/api-guide/versioning/
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
        'DEFAULT_VERSION': '1.0',
        'ALLOWED_VERSIONS': ['1.0', ],
        'VERSION_PARAMETER': 'version',


        # Use hyperlinked styles by default.
        # Only used if the `serializer_class` attribute is not set on a view.
        'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            # Mainly used by amigo-ios
            "amigo.auth.backends.Token",

            # Mainly used for api debug.
            "amigo.auth.backends.Session",
        ),
        "EXCEPTION_HANDLER": "amigo.base.exceptions.exception_handler",
    }

    # MIGRATIONS CONFIGURATION
    # ------------------------------------------------------------------------------
    MIGRATION_MODULES = {
        'zeropush': 'amigo.zeropush.migrations'
    }

    # Django Rest Framework
    PUBLIC_REGISTER_ENABLED = env.bool('DJANGO_PUBLIC_REGISTER_ENABLED',
                                       default=True)

    USE_ETAGS = True

    # Authentication
    AUTH_USER_MODEL = "users.User"

    # Amigo
    AMIGO_APPSTORE_URL = env("AMIGO_APPSTORE_URL", default='http://amigo.io')
    AMIGO_APP_URL_SCHEME = env("AMIGO_APP_URL_SCHEME", default='amigo')
    HOURS_TO_EVENT_DEACTIVATATION = 12

    DEFAULT_AVATAR_SIZE = 60                # 60x60 pixels
    DEFAULT_BIG_AVATAR_SIZE = 250           # 250x250 pixels
    VERSATILEIMAGEFIELD_SETTINGS = {
        # The amount of time, in seconds, that references to created images
        # should be stored in the cache. Defaults to `2592000` (30 days)
        'cache_length': 2592000,
        # The name of the cache you'd like `django-versatileimagefield` to use.
        # Defaults to 'versatileimagefield_cache'. If no cache exists to the name
        # provided, the 'default' cache will be used.
        'cache_name': 'vif_cache',
        # The save quality of modified JPEG images. More info here:
        # http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#jpeg
        # Defaults to 70
        'jpeg_resize_quality': 95,
        # A path on disc to an image that will be used as a 'placeholder'
        # for non-existant images.
        # If 'global_placeholder_image' is unset, the excellent, free-to-use
        # http://placehold.it service will be used instead.
        'global_placeholder_image': None,
        # The name of the top-level folder within your storage to save all
        # sized images. Defaults to '__sized__'
        'sized_directory_name': "_s_",
        # The name of the directory to save all filtered images within.
        # Defaults to '__filtered__':
        'filtered_directory_name': "_f_"
    }

    # TWILIO Configuration
    # see: https://www.twilio.com/user/account
    TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID', default='')
    TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN', default='')
    TWILIO_PHONE_NUMBER = env('TWILIO_PHONE_NUMBER', default='')

    TWILIO_CALLBACK_DOMAIN = env('TWILIO_CALLBACK_DOMAIN', default='')
    TWILIO_CALLBACK_USE_HTTPS = env('SITE_SCHEME', default="http")
    TWILIO_DRY_MODE = env('TWILIO_DRY_MODE', default=False)
    TWILIO_SKIP_SIGNATURE_VALIDATION = env('TWILIO_SKIP_SIGNATURE_VALIDATION',
                                           default=False)
    SMS_VALIDATION_LENGTH = 4
    SMS_VALIDATION_MESSAGE = ("Presto! {} is your secret code to verify"
                              " or tap this link to login: " + AMIGO_APP_URL_SCHEME + "://verify/{}")

    # Invite template
    SMS_INVITE_TEMPLATE = ("{user_name} is using Amigo to make it easier to get together with friends and "
                           "thinks you should join too! Get the app here: {app_store_link}")
    # -------- SMS configuration

    # ZERO PUSH
    ZEROPUSH_AUTH_TOKEN = env('ZEROPUSH_AUTH_TOKEN', default='')
    DISABLE_PUSH_NOTIFICATION = False
    ENVIRONMENT = ''

    CACHE_KEYS = {
        'event_invitee_photo_urls': 'event_i_p_urls:{event_id}'
    }

    # Analytics
    # -------------------------------------------------------------------------
    MIXPANEL_PROJECT_TOKEN = env('MIXPANEL_PROJECT_TOKEN', default='')

    # CACHING
    # ------------------------------------------------------------------------------
    CACHES = {
        'default': {
            'BACKEND': 'redis_lock.django_cache.RedisCache',
            "LOCATION": "{0}/{1}".format(env('REDISTOGO_URL', default="redis://localhost:6379").strip("/"), 0),
            'OPTIONS': {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # mimics memcache behavior.
                # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
                "IGNORE_EXCEPTIONS": env.bool('CACHE_IGNORE_EXCEPTIONS', default=False),
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 50,
                    'timeout': 20,
                },
            }
        }
    }

    # Most Common Time Zones
    TZ_DETECT_COUNTRIES = ('CN', 'US', 'IN', 'JP', 'BR', 'RU', 'DE', 'FR', 'GB')

    GRAPPELLI_ADMIN_TITLE = "Amigo Administration"

    # Airbrake settings
    AIRBRAKE = {
        'API_KEY': 'b57181ddbc5fee66b42ee8b16fc39d61',
        'API_URL': 'https://airbrake.io/',
        'USE_SSL': True,
        'TIMEOUT': 5,
        'ENVIRONMENT': 'production',
    }

    # Uservoice settings
    USERVOICE_SUBDOMAIN_NAME = env('USERVOICE_SUBDOMAIN_NAME', default='')
    USERVOICE_API_KEY = env('USERVOICE_API_KEY', default='')
    USERVOICE_API_SECRET = env('USERVOICE_API_SECRET', default='')
    USERVOICE_SSO_KEY = env('USERVOICE_SSO_KEY', default='')
    USERVOICE_URL = env('USERVOICE_URL', default='')
