import os
from django.urls import path
from .views import stats_proceed_view, GamesDetailView, GamesListView, GamesAddView
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

stats_bot_token = os.getenv("STATS_BOT_TOKEN_TEST")

app_name = 'games'

urlpatterns = [
    path('', GamesListView.as_view(), name='games_index'),
    path('<int:pk>/', GamesDetailView.as_view(), name='games_detail'),
    path('add_game/', GamesAddView.as_view(), name='add_game'),
    path('stats_proceed/' + stats_bot_token, stats_proceed_view, name='stats_proceed_from_bot'),
]
