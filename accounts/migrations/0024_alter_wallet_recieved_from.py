# Generated by Django 4.2.6 on 2023-11-27 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_subscription_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='recieved_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieved_transactions', to=settings.AUTH_USER_MODEL),
        ),
    ]
