# Generated by Django 4.2.6 on 2023-11-16 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_premiumuserinfo_bank_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiumuserinfo',
            name='linkedin_url',
            field=models.CharField(default='skdcbkasbckaskcxbk', max_length=100),
        ),
    ]
