# Generated by Django 3.2 on 2021-05-10 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210510_1840'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendshiprequest',
            unique_together={('from_user', 'to_user', 'is_rejected', 'is_accepted')},
        ),
    ]