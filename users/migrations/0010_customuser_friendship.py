# Generated by Django 3.2 on 2021-05-02 19:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210327_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='friendship',
            field=models.ManyToManyField(related_name='_users_customuser_friendship_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
