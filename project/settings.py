from dotenv import load_dotenv
from pathlib import Path
import os
import dj_database_url # تأكد من استيراد هذه المكتبة

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# استخدم متغير بيئة للمفتاح السري
SECRET_KEY = os.environ.get('SECRET_KEY')
# تأكد من أن المفتاح السري موجود لتجنب المشاكل في الإنتاج
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set.")

# تحديد وضع DEBUG بناءً على بيئة النشر
# إذا كان DATABASE_URL موجودًا (كما في Vercel)، فنحن في الإنتاج (DEBUG=False)
# وإلا، فنحن في التطوير المحلي (DEBUG=True)
IS_PRODUCTION_ENV = os.environ.get('DATABASE_URL') is not None

if IS_PRODUCTION_ENV:
    DEBUG = False
else:
    DEBUG = True # تفعيل DEBUG للتطوير المحلي (مهم لعرض الملفات الثابتة والوسائط)

# سمح بالوصول من نطاقات Vercel والتطوير المحلي
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']
# يمكنك لاحقًا إضافة اسم النطاق المخصص الخاص بك هنا إذا كان لديك
# مثال: ALLOWED_HOSTS = ['.vercel.app', 'www.yourdomain.com', 'yourdomain.com', 'localhost', '127.0.0.1']


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
    # لا تنسى تشغيل `pip install whitenoise` إذا لم تكن قد فعلت ذلك بالفعل
    # وتحديث ملف requirements.txt
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # أضف WhiteNoise هنا لخدمة الملفات الثابتة بكفاءة في الإنتاج
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

WSGI_APPLICATION = 'project.wsgi.application' # تأكد أن هذا يشير إلى 'application' وليس 'app' هنا

# Database
# استخدام PostgreSQL مع متغيرات البيئة للإنتاج، و SQLite3 للتطوير المحلي
# يجب أن يكون DATABASE_URL موجودًا في متغيرات بيئة Vercel (أو في ملف .env محليًا للاتصال بـ Supabase من local)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL: # إذا كان متغير DATABASE_URL موجودًا (مثل على Vercel)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600  # للحفاظ على الاتصالات نشطة
        )
    }
else: # إذا لم يكن موجودًا (على جهازك المحلي)
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


# إعدادات الملفات الثابتة (Static Files) للإنتاج
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles') # هذا المجلد هو المكان الذي سيتم تجميع الملفات الثابتة فيه في الإنتاج
STATIC_URL = '/static/' # تأكد من أن هذا يبدأ بشرطة مائلة

# هذا يخبر Django أين يبحث عن ملفاتك الثابتة (CSS, JS, صور التصميم)
# 'static' يشير إلى مجلد 'static' في جذر مشروع Django الخاص بك
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static') # <--- تم تعديل هذا السطر!
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'


MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/' # تأكد من أن هذا يبدأ بشرطة مائلة
