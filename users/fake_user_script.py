import sys
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'Metrica_project.settings'  # set Django-needed settings module
django.setup()

from faker import Faker
from faker.providers import internet, person, misc
from users.models import CustomUser


def fake_users(iteration):
    fake = Faker()
    fake.add_provider(internet)
    fake.add_provider(person)
    fake.add_provider(misc)
    for _ in range(iteration):
        CustomUser.objects.create_user(username=fake.user_name(), first_name=fake.first_name(),
                                       last_name=fake.last_name(), password=fake.password(), email=fake.ascii_email())
    print(f'{iteration} fake-users are created')


if __name__ == '__main__':
    fake_users(int(sys.argv[1]))
