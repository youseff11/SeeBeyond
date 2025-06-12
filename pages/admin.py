from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db import models
from .models import Profile, Order, OrderItem


# 1. Inline لعرض البروفايل داخل اليوزر
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
        return "-"
    phone_number_display.short_description = 'Phone Number'
    phone_number_display.admin_order_field = 'profile__phone_number'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# 2. Inline لعرض المنتجات داخل الطلب
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


# 3. Admin للطلب
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_ordered', 'status', 'colored_status', 'display_total_price', 'transaction_id']
    list_filter = ['status', 'date_ordered']
    search_fields = ['id', 'user__username', 'transaction_id']
    inlines = [OrderItemInline]
    readonly_fields = ['date_ordered', 'transaction_id']
    list_editable = ['status']  # التحكم المباشر
    actions = ['mark_completed', 'mark_shipped', 'mark_cancelled']

    # لجمع السعر من المنتجات
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _total_price=models.Sum(
                models.F('orderitem__price_at_order') * models.F('orderitem__quantity'),
                output_field=models.DecimalField()
            )
        )

    def display_total_price(self, obj):
        if hasattr(obj, '_total_price') and obj._total_price is not None:
            return f"${obj._total_price:.2f}"
        return f"${obj.total_price:.2f}"
    display_total_price.admin_order_field = '_total_price'
    display_total_price.short_description = 'Total Price (Calculated)'

    # عرض الحالة بلون مخصص
    def colored_status(self, obj):
        color_map = {
            'pending': '#facc15',     # أصفر
            'processing': '#38bdf8',  # أزرق فاتح
            'shipped': '#34d399',     # أخضر فاتح
            'completed': '#10b981',   # أخضر
            'cancelled': '#f87171',   # أحمر
        }
        color = color_map.get(obj.status, '#d1d5db')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 6px;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status (Colored)'
    colored_status.admin_order_field = 'status'

    # إجراءات لتغيير الحالة من الأكشن فوق
    @admin.action(description="Mark selected orders as Completed")
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description="Mark selected orders as Shipped")
    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')

    @admin.action(description="Mark selected orders as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
