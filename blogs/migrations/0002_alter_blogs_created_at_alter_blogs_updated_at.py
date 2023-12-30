# Generated by Django 4.2.6 on 2023-11-10 11:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
