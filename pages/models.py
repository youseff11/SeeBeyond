from django.db import models
from django.contrib.auth import get_user_model 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from decimal import Decimal
from products.models import Product

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['-date_ordered']
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total.quantize(Decimal('0.01'))

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.quantity for item in orderitems)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date_added = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.product.name} ({self.quantity}) in Order {self.order.id}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    @property
    def get_total(self):
        return (self.price_at_order * self.quantity).quantize(Decimal('0.01'))

# --- New Profile Model and Signals ---

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True) # New field for phone number

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()