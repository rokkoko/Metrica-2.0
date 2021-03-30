import datetime as date
from games.db_actions import stats_repr, add_scores, get_game_names_list, get_game_id_by_name
from .income_msg_parser import parse_message
from telegram import Bot, Update, ForceReply
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import requests


REGISTRATION_URL = 'https://d62d53c99f46.ngrok.io/users/add_user/'
ADD_GAME_URL = 'https://d62d53c99f46.ngrok.io/games/add_game_from_bot/'

class StatsBot:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher(self.bot, None, workers=0)
        self.dispatcher.add_handler(CommandHandler("add", add_stats_command))
        self.dispatcher.add_handler(CommandHandler("show", show_stats_command))
        self.dispatcher.add_handler(CommandHandler("register", register_user_command))
        self.dispatcher.add_handler(CommandHandler("add_game", add_game_command))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, process_photo_message))
        self.dispatcher.add_handler(
            MessageHandler(~Filters.command, process_bot_reply_message))

    def process_update(self, request):
        update = Update.de_json(request, self.bot)
        print('Update decoded', update.update_id)
        self.dispatcher.process_update(update)
        print('Stats request processed successfully', update.update_id)

def add_game_command(update, context):
    context.user_data["last_command"] = "GAME"
    update.message.reply_text(
        f'Добавить игру',
        reply_markup=ForceReply())

def process_add_game_command(update, context):
    game = update.message.text
    response = requests.post(REGISTRATION_URL, json={"game_name": str(game)})
    update.message.reply_text(response.text)


def process_photo_message(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('avatar.jpg')


def register_user_command(update, context):
    # Store the command in context to check later in message processors
    context.user_data["last_command"] = "REGISTER"
    update.message.reply_text(
        f'Зарегистрировать юзера',
        reply_markup=ForceReply())

def register_command(update, context):
    user = update.message.text
    response = requests.post(REGISTRATION_URL, json={"user": str(user)})
    update.message.reply_text(response.text)

def add_stats_command(update, context):
    # Store the command in context to check later in message processors
    context.user_data["last_command"] = "ADD"
    update.message.reply_text(
        f'Добавить статы для активности (уже зарегистрированные: {", ".join(get_game_names_list())})',
        reply_markup=ForceReply(selective=True))


def show_stats_command(update, context):
    # Store the command in context to check later in message processors
    context.user_data["last_command"] = "SHOW"
    update.message.reply_text(
        f'Показать статы для активности (уже зарегистрированные: {", ".join(get_game_names_list())})',
        reply_markup=ForceReply(selective=True))


def process_unknown_message(update, context):
    update.message.reply_text('В эту игру вы еще не шпилили')


def process_wrong_message(update, context):
    update.message.reply_text('Не получилось обработать запрос')


def is_scores_message(update):
    return ':' in update.message.text


def is_known_activity_message(update):
    game = parse_message(update.message.text)
    return True if get_game_id_by_name(game) else False


def process_bot_reply_message(update, context):
    last_command = context.user_data["last_command"]

    if last_command == 'ADD' and is_scores_message(update):
        process_add_stats_message(update, context)
    elif last_command == 'SHOW':
        if is_scores_message(update):
            process_wrong_message(update, context)

        elif is_known_activity_message(update):
            process_show_stats_message(update, context)
        else:
            process_unknown_message(update, context)
    elif last_command == 'REGISTER':
        register_command(update, context)
    elif last_command == 'GAME':
        process_add_game_command(update, context)


def process_show_stats_message(update, context):
    data = update.message.text
    game = parse_message(data)
    score_pairs = stats_repr(game)

    if isinstance(score_pairs, dict):
        result_dict = score_pairs

    result_msg = f'На {date.datetime.today().replace(microsecond=0)} ' \
                 f'по игре "{game}" {"общие статы ВСЕХ игрокококов такие"}:\n'
    for user_name, score in result_dict.items():
        result_msg += user_name + ': ' + str(score) + '\n'

    update.message.reply_text(result_msg)


def process_add_stats_message(update, context):
    data = update.message.text
    game, score_pairs = parse_message(data)
    result_dict = add_scores(game, score_pairs)
    if isinstance(result_dict, str):
        negative_score_msg = result_dict
        update.message.reply_text(negative_score_msg)
        return

    result_msg = f'На {date.datetime.today().replace(microsecond=0)} ' \
                 f'по игре "{game}" {"статы для текущих игрококов"}:\n'
    for user_name, score in result_dict.items():
        result_msg += user_name + ': ' + str(score) + '\n'

    update.message.reply_text(result_msg)
