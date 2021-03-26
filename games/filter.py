import django_filters
from games.models import Games, GameSession
from users.models import CustomUser


class GamesFilter(django_filters.FilterSet):
    game = django_filters.ModelChoiceFilter(queryset=Games.objects.all())
    created_at = django_filters.NumberFilter(
        label='month played game',
        method='get_month',

    )
    scores__user = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all(),
    )

    def get_month(self, queryset, field_name, month):
        return queryset.filter(created_at__month=month)

    def get_user(self, queryset, field_name, user):
        return queryset.filter(scores__user=user)

    class Meta:
        model = GameSession
        fields = ["game", "created_at"]