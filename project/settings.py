from dotenv import load_dotenv
from pathlib import Path
import os
import dj_database_url

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# استخدم متغير بيئة للمفتاح السري
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set.")

# تحديد وضع DEBUG بناءً على بيئة النشر
IS_PRODUCTION_ENV = os.environ.get('DATABASE_URL') is not None

if IS_PRODUCTION_ENV:
    DEBUG = False
else:
    DEBUG = True

# سمح بالوصول من نطاقات Vercel والتطوير المحلي
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'contact.apps.ContactConfig',
    'products.apps.ProductsConfig',
    'pages.apps.PagesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.app' # تأكد أن هذا يشير إلى 'app' هنا


# Database
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# إعدادات الملفات الثابتة (Static Files)
# STATIC_ROOT: حيث يقوم collectstatic بتجميع جميع الملفات الثابتة في الإنتاج
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles') 

# STATIC_URL: المسار الأساسي لخدمة الملفات الثابتة عبر الويب
STATIC_URL = '/static/' 

# STATICFILES_DIRS: قائمة المجلدات الإضافية التي يجب على Django البحث فيها عن الملفات الثابتة.
# هذا يشير إلى مجلد 'static' الموجود داخل مجلد 'project' الرئيسي.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'project', 'static') 
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'


MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
