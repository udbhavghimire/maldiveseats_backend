# Generated by Django 5.1.7 on 2025-03-22 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maldives_eats', '0002_order_orderitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
