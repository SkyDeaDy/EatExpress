# Generated by Django 4.2.9 on 2024-03-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0008_remove_cart_users_cart_user_alter_cartitem_dish_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(null=True, to='delivery_app.cartitem'),
        ),
    ]
