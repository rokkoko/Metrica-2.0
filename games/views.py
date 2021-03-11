import os
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from games.db_actions import get_game_id_by_name, get_game_object_by_id, \
    add_game_into_db, add_game_session_into_db, add_scores
from Metrica_project.stats_bot import StatsBot

stats_bot_token = os.getenv("STATS_BOT_TOKEN")


def stats_proceed_view(request):
    stats_bot = StatsBot(stats_bot_token)

    # LOGIC
    request_json = json.loads(request.body)
    stats_bot.process_update(request_json)


    return HttpResponse()  # view ALWAYS must return response