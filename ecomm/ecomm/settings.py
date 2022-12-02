

from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    DEBUG=(bool, False)
)


environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.

TEMPLATES_DIR = os.path.join(BASE_DIR , 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY')
SECRET_KEY='django-insecure-gzf(u4qg80w047^c2@+nw(s&tb-ltde=sv1+7rqz3-0aid7w*('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.CustomUserModel'
# Application definition

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]


CUSTOM_APPS = [
    'accounts',
    'home',
    'Email_Template',
    'products',
    'mptt',
    'crispy_forms',
    'anymail'
]


THIRD_PARTY_APPS = [
    'django_filters'
]


INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'products.middlewares.auth.auth_middleware',
    'base.middlewares.auth.RestrictAdminUserInFrontend'

    
]

LOGIN_URL = 'login'

ROOT_URLCONF = 'ecomm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.context_processor.extras'
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'emart',
       'USER': 'postgres',
       'PASSWORD':'ROOT',
       'HOST': 'localhost',
       'PORT': '5432',
   }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_TZ = True

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATIC_DIR = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = [STATIC_DIR,]

# STATICFILES_DIR = {
#     os.path.join(BASE_DIR , "static")
# }


MEDIA_ROOT =  os.path.join(BASE_DIR, 'static') 
MEDIA_URL = '/media/'


#my email sending varibles

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = "sohailbadeghar561@gmail.com"
EMAIL_HOST_PASSWORD = "zgqigddcshicekca"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'ashishdede11@gmail.com'
# EMAIL_HOST_PASSWORD = 'gjjkatlltvdkhzao'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# SENDGRID_API_KEY = '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'
# SENDGRID_API_KEY = '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'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LOGIN_REDIRECT_URL ='homepage'
LOGOUT_REDIRECT_URL ='homepage'

KEY_ID = 'rzp_test_hW4cPfpr8uPIqe'
KEY_SECRET = 'IQ4XzmySHE8RoeGxidSO3fkt'


CRISPY_TEMPLATE_PACK = 'bootstrap4'

    # merchant_id=str(os.getenv("BT_MERCHANT_ID")),
        # public_key=str(os.getenv("BT_PUBLIC_KEY")),
        # private_key=str(os.getenv("BT_PRIVATE_KEY"))

# STRIPE_PUBLIC_KEY=env('STRIPE_PUBLIC_KEY')

# STRIPE_SECRET_KEY=env('STRIPE_SECRET_KEY')

MERCHANT_ID ='f49w49kxcr7dhx3p'
PUBLIC_KEY='5g29t22hfk42zk2d'
PRIVATE_KEY='b252c6e805ae98e5735610fdb76eda8e'



STRIPE_PUBLIC_KEY='pk_test_51LugK4SBvpMZRuEMRahPDfnrLIIKHuoGKGvbQnSK4By0B5QOOmIdVfyRtwSuEH35o6T1EhGFq4flQWSbLJZN1X3900JigQfS5Q'
STRIPE_SECRET_KEY='sk_test_51LugK4SBvpMZRuEMr93TljkDqDZLpLH7TnrruLcwNZBMNRVdlxJ2j9vaUKC1IkRS4weKYjEVjogFMKKFuAOiCGI600D9XYMcXd'

STRIPE_WEBHOOK_SECRET='whsec_d5c3048b6ade8fbd90334ea542dca0f37e63728d1c7fdc678fa3e3ad0aa5b2cb'



# EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
# SENDGRID_SANDBOX_MODE_IN_DEBUG=False
# channel 
# coding for enterpreneur
# just for django 
# denis ivy 




# ANYMAIL = {
#     "MAILGUN_API_KEY": "<your Mailgun key>",
# }

# EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"  # or sendgrid.SendGridBackend, or...
FROM_EMAIL = 'sohailbadeghar561@gmail.com'





# pass - 'sunil@1995sunil@1995'




# Hobby is an activity that we enjoy doing in our free time. 
# It keeps us busy in our leisure time .
# People choose their hobbiees on the basis of their interests and personality. 
# Do you know what Dr. A.P.J Abdul Kalam'shobby was ?



# proper noun - Abdul kalam
# common noun - acitvity
# collective noun - People 