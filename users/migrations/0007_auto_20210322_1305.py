# Generated by Django 3.1.7 on 2021-03-22 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
