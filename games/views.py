import logging
import os
import uuid
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count

from Metrica_project.storage_backends import MediaStorage
from games.models import Games, GameScores, GameSession
from games.forms import GameCreationForm
from games.utils import game_cover_double_reducer
from users.models import CustomUser

from games.db_actions import get_game_id_by_name, get_user_list_for_current_game, \
    get_users_with_scores
from games.filter import GameFilter


logger = logging.getLogger("Metrica_logger")


class GamesDetailView(DetailView):
    model = Games
    template_name = 'games_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        users = CustomUser.objects.prefetch_related("scores") \
            .filter(
            scores__game_session__game__id=self.kwargs["pk"],
        ).annotate(played_public_games_count=Count("scores__game_session"))

        user_list_for_current_game = get_user_list_for_current_game(
            users,
            self.request.user.pk,
            self.kwargs["pk"]
        )

        context['played_games_by_players'] = user_list_for_current_game

        private_sessions = GameSession.objects.prefetch_related("scores") \
            .filter(
            game__id=self.kwargs["pk"],
            is_private=True,
            scores__user__pk=self.request.user.pk
        )

        context['private_sessions'] = list(map(lambda session: dict(
            session=session,
            score=GameScores.objects.get(
                game_session=session,
                user=self.request.user.pk
            ).score
        ), private_sessions))

        users_with_scores = get_users_with_scores(
            self.request.user.pk,
            user_list_for_current_game,
            self.kwargs['pk']
        )

        context["users"] = users_with_scores

        # We put this to server data as JSON and read from Javascript side
        context['server_data'] = {
            "users": users_with_scores
        }

        return context


# per-view caching (method decorator to convert view decorator to method of the class.
# For cache framework need acces to request, so method of the class should contained it.
# In 'list'-CBV one of that method - is 'get')
# @method_decorator(cache_page(120, cache='fs_cache'), name='get')
class GamesListView(ListView):
    model = Games
    template_name = 'games_index.html'
    context_object_name = 'games'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["filter"] = GameFilter(
            self.request.GET)

        for game in Games.objects.all():
            context[game.name] = CustomUser.objects.filter(scores__game_session__game__name=game.name).distinct()

        if self.request.user.is_authenticated:
            if self.request.GET.get('self_game_sessions') == "on":
                context['filter'] = GameFilter(
                    self.request.GET,
                    queryset=Games.objects.filter(sessions__scores__user=self.request.user).distinct()
                )

        return context


class GamesAddView(CreateView):
    model = Games
    form_class = GameCreationForm
    template_name = 'add_game.html'

    def post(self, request, *args, **kwargs):
        """
        Reduce incoming users game_cover images
        """
        if request.FILES.get("cover_art"):
            game_cover = request.FILES["cover_art"]
            request.FILES["cover_art"] = game_cover_double_reducer(game_cover)

        return super().post(request, args, kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class GamesAddBotView(View):

    def post(self, request):
        game_name = request.POST["game_name"]

        if request.FILES.get("avatar"):
            game_cover_file = game_cover_double_reducer(request.FILES["avatar"])
            dirs_by_date = datetime.now().strftime('/%Y/%m/%d/')
            file_directory_within_bucket = f"uploads/games_cover/{dirs_by_date}"
            game_cover_file.name = f"{uuid.uuid4()}.jpg"
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                game_cover_file.name
            )

            media_storage = MediaStorage()  # settings_prod case
            media_storage.save(file_path_within_bucket, game_cover_file)

            Games.objects.create(name=game_name, cover_art=file_path_within_bucket)

        else:
            Games.objects.create(name=game_name)

        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class GameCheck(View):
    def get(self, request):
        game_name = request.GET.get("game_name")
        result = {"exist_game": get_game_id_by_name(game_name)}

        return JsonResponse(result)
