# Generated by Django 4.2.6 on 2023-11-22 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_rename_subscription_price_premiumuserinfo_subscription_price_basic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='subscription_type',
            field=models.CharField(choices=[('basic', 'Basic'), ('standard', 'Standard')], max_length=10),
        ),
    ]
