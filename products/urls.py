# products/urls.py
from django.urls import path
from . import views # استورد views من نفس التطبيق

urlpatterns = [
    path('', views.shop, name='shop'), # مسار لصفحة عرض المنتجات
    path('<int:product_id>/', views.product_detail, name='product_detail'), # مسار لتفاصيل منتج معين
]