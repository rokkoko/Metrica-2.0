import django_filters
from games.models import Games, GameSession


class GamesFilter(django_filters.FilterSet):

    class Meta:
        model = Games
        fields = ["name",]