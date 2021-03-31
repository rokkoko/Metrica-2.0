from datetime import datetime
from django.db.models import Sum
from users.models import CustomUser
from .models import Games, GameScores, GameSession
from .checkup import negative_score_check
from users.db_actions import get_username_by_id
from users.db_actions import add_user_into_db_from_score_pairs
from users.db_actions import get_user_object_by_id


def get_game_id_by_name(name):
    """
    :param name: str()-repr of game name
    :return: id of the game from db. In case when game is not in db - return False
    """
    try:
        game_id = Games.objects.get(name=name).pk
    except Exception:
        return False
    return game_id


def get_game_names_list():
    """
    :return: list() of names of all games in db
    """
    queryset = Games.objects.all()
    _list = [elem.name for elem in queryset]
    return _list



def get_game_object_by_id(game_id):
    """
    :param game_id: int() id of the game in db
    :return: model.object (row from table) of the game.
    In case when game is not in db - return False
    """
    try:
        game = Games.objects.get(id=game_id)
    except Exception:
        return False
    return game


def add_game_into_db(name):
    """
    Insert new game into db
    :param name: str()-name of the game
    :return: model object of new added game
    """
    game = Games.objects.get_or_create(name=name)[0]
    return game


def add_game_into_db_single_from_bot(name, data):
    """
    Insert new game into db
    :param name: str()-name of the game
    :return: model object of new added game
    """
    with open('test3.jpg', 'wb+') as f:
        f.write(data)
        f.close()

# Тут для поля ImageFiled просто указываем путь на скачанную аватарку.
# Для этого предварительно сохраняем переданное изображение.
# Т.к. бот у нас отправялет json и view его парсит (json.loads()), то нам
# request'ом нужно передать json. Чтобы в него вставить файл - кодирую его
# base64. ПРОБЛЕМА в том, что сериализация типов bytes (а это именно он в base64)
# не поддерживается. А преобразовав этот тип в str() в строке 63 не происходит
# корректная запись инфы в файл. Но все остальное работает (содается объект модели
# и хаполняется поле ImageField ссылкой на битый файл)

    game = Games.objects.get_or_create(name=name, cover_art='test3.jpg')

    if game[1]:
        print(f"New game '{name}' added to Metrica!")
    else:
        print(f"Game '{name}' already tracking by Metrica")
    return game[1]


def add_game_session_into_db(game):
    """
    Insert new game session object (row) into db
    :param game: model.object (row from db Games)
    :return: id of new game session object
    """
    date = datetime.now()
    game_session_object = GameSession.objects.create(
        game=game,
        created_at=date,
    )
    return game_session_object


def add_scores(game_name, score_pairs: dict):
    """
    Insert row (object) in table (model) GameScores from parsed income msg.
    :param game_name: str(name of the game)
    :param score_pairs: dict(str(username): int(score))
    :return: dict(str(username): sum(int(score)))
    """
    try:
        negative_score_check(score_pairs)
    except ValueError:
        return "Negative score is impossible"

    game = add_game_into_db(game_name)
    game_session_object = add_game_session_into_db(game)
    users_ids = add_user_into_db_from_score_pairs(score_pairs)
    result_msg_dict = dict()

    for user_id in users_ids:
        user = get_user_object_by_id(user_id)
        username = user.username
        GameScores.objects.create(
            game_session=game_session_object,
            user=user,
            score=score_pairs[username],
        )
        result_msg_dict[username] = \
            GameScores.objects.filter(game_session__game=game).filter(user=user).aggregate(Sum('score'))['score__sum']
    return result_msg_dict


def stats_repr(game):
    """
    :param game: str(name of the game)
    :return: sum of all scores all-played users in 'game': dict(str(username): sum(int(score)))
    """
    game_id = get_game_id_by_name(game)
    game_object = get_game_object_by_id(game_id)
    if not game_id:
        return f'В игру "{game}" Вы еще не играли. Статистика отсутствует.'
    users_ids = [i.id for i in CustomUser.objects.filter(scores__game_session__game=game_object).distinct()]
    result_msg_dict = dict()
    for user_id in users_ids:
        user = get_user_object_by_id(user_id)
        username = get_username_by_id(user_id)
        result_msg_dict[username] = \
            GameScores.objects.filter(
                game_session__game=game_object
            ).filter(user=user).aggregate(Sum('score'))['score__sum']
    return result_msg_dict