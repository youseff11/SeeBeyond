from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Order, OrderItem # تأكد ان كل موديلزك هنا
from django.db import models


# 1. Admin setup for Profile (Inline with User)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = BaseUserAdmin.list_display + ('phone_number_display',)

    def phone_number_display(self, obj):
        if hasattr(obj, 'profile') and obj.profile.phone_number:
            return obj.profile.phone_number
        return "-" # لو مفيش رقم تليفون، يعرض شرطة
    phone_number_display.short_description = 'Phone Number' # اسم العمود في القائمة
    phone_number_display.admin_order_field = 'profile__phone_number' # عشان تقدر ترتب القائمة برقم التليفون

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 2. Admin setup for Order and OrderItem (Existing code)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_ordered', 'complete', 'display_total_price', 'transaction_id']
    list_filter = ['complete', 'date_ordered']
    search_fields = ['id', 'user__username', 'transaction_id']
    inlines = [OrderItemInline]
    readonly_fields = ['date_ordered', 'transaction_id']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _total_price=models.Sum(
                models.F('orderitem__price_at_order') * models.F('orderitem__quantity'),
                output_field=models.DecimalField()
            )
        )

    def display_total_price(self, obj):
        if obj._total_price is not None:
            return f"${obj._total_price:.2f}"
        return f"${obj.total_price:.2f}"
    display_total_price.admin_order_field = '_total_price'
    display_total_price.short_description = 'Total Price (Calculated)'