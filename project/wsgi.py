import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# هذا هو متغير WSGI القياسي في Django، ويستخدمه خادم التطوير المحلي (runserver).
application = get_wsgi_application()

# هذا هو متغير WSGI البديل الذي تتوقعه بعض بيئات النشر مثل Vercel.
# نقوم بجعله يشير إلى تطبيق Django الرئيسي.
app = application