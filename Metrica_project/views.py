from users.models import CustomUser
from django.shortcuts import render


def index(request):
    names = map(lambda user: user.username, CustomUser.objects.distinct())

    return render(request, 'metrica_index.html', context={"serverData": {
        "data": [12, 19, 3, 5, 2, 3],
        "labels": list(names)
    }})
