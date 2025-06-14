# Generated by Django 5.2.2 on 2025-06-12 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_remove_order_status_order_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='complete',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
