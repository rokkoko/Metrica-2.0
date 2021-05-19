import django_filters


class IncomeFriendshipRequestFilter(django_filters.FilterSet):
    is_accepted = django_filters.BooleanFilter(
        lookup_expr='exact',
        label='принятые запросы',
        field_name='is_accepted',
    )

    is_rejected = django_filters.BooleanFilter(
        lookup_expr='isnull',
        label='не рассмотренные запросы',
        field_name='is_accepted',
    )
