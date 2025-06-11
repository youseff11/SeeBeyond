# pages/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # مسارات تسجيل الدخول والتسجيل والخروج
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # مسارات الصفحات الثابتة وحساب المستخدم
    path('policies/', views.policies, name='policies'),
    path('account/', views.account, name='account'),
    path('account/add_address/', views.add_address, name='add_address'),

    # مسارات سلة التسوق والطلبات
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_summary_view, name='cart_summary'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('process-order/', views.process_order, name='process_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]