# Generated by Django 3.1.7 on 2021-03-16 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0003_auto_20210316_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamescores',
            name='game_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='games.gamesession'),
        ),
        migrations.AlterField(
            model_name='gamescores',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='game',
            field=models.ForeignKey(default='default_game', on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='games.games'),
        ),
    ]
