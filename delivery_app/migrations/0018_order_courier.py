# Generated by Django 4.2.9 on 2024-03-25 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0005_remove_profile_first_name_remove_profile_last_name_and_more'),
        ('delivery_app', '0017_alter_order_created_at_delete_courier'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile_app.courier'),
        ),
    ]
