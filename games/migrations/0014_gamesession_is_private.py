# Generated by Django 3.2 on 2021-05-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0013_auto_20210402_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesession',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
