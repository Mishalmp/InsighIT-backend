# Generated by Django 4.2.6 on 2023-11-17 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_blogs_is_premium'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogs',
            old_name='is_premium',
            new_name='is_premium_blog',
        ),
    ]
