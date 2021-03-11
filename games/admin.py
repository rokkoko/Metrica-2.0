from django.contrib import admin
from .models import Games, GameSession, GameScores


admin.site.register(Games)
admin.site.register(GameSession)
admin.site.register(GameScores)