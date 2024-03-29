# Generated by Django 4.2.9 on 2024-03-06 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery_app', '0007_remove_cart_user_remove_cartitem_user_cart_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='users',
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='dish_id',
            field=models.IntegerField(),
        ),
    ]
