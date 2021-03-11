from users.models import CustomUser


def get_username_by_id(id: int):
    """
    :param id: int(id) of requested user
    :return: str__repr of model object (username)
    """
    result = CustomUser.objects.get(id=id).username
    return result


def get_user_object_by_id(id):
    """
    :param user_id: int() id of the user in db
    :return: model.object (row from table) of the user.
    In case when game is not in db - return False
    """
    try:
        user_object = CustomUser.objects.get(id=id)
    except Exception:
        user_object = False
    return user_object


def get_user_id_by_name(name):
    """
    :param name: str() name of requested user
    :return: int()-id of requested user
    """
    result = CustomUser.objects.get(username=name).pk
    return result


def add_user_into_db_simple(username):
    new_user = CustomUser.objects.get_or_create(username=username)[0].pk
    print(f'New user "{username}" added to db. WELCOME!')
    return new_user


def add_user_into_db_from_score_pairs(score_pairs:dict):
    '''
    :param score_pairs: dict {"username": score:int}
    :return: list of id's new users added to db
    '''
    new_users_id_list = []
    for username in score_pairs.keys():
        if CustomUser.objects.get_or_create(username=username)[1]:
            new_users_id_list.append(CustomUser.objects.get_or_create(username=username)[0].id)
            print(f'{username} added to DB')
        else:
            print(f'{username} already in DB')
    return new_users_id_list
