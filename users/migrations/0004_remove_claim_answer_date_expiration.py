# Generated by Django 3.1.7 on 2021-03-20 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210320_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='answer_date_expiration',
        ),
    ]