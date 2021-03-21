from django.shortcuts import render


def index(request):
    return render(request, 'metrica_index.html', context={"serverData": [12, 19, 3, 5, 2, 3]})
