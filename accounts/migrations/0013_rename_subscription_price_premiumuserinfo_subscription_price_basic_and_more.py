# Generated by Django 4.2.6 on 2023-11-22 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='premiumuserinfo',
            old_name='subscription_price',
            new_name='subscription_price_basic',
        ),
        migrations.AddField(
            model_name='premiumuserinfo',
            name='subscription_price_std',
            field=models.DecimalField(decimal_places=2, default=75, max_digits=10),
        ),
    ]
