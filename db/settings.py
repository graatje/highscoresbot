import os
import dotenv

dotenv.load_dotenv()
from django.core.management import execute_from_command_line


def init_django():
    print("initializing django")
    import django
    from django.core.wsgi import get_wsgi_application
    from django.conf import settings

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=[
            'db.ingame_data',
            'db.config',
            'db.highscores',
            'db.eventconfigurations'
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'pokemon_planet_api',
                'USER': os.environ.get("PGUSERNAME"),
                "PASSWORD": os.environ.get("PASSWORD"),
                "HOST": "127.0.0.1",
                "PORT": 5432
            }
        },
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        SECRET_KEY='django-insecure-$cd9u9q)e%7+v7gg#g1ulnr^d18qq%z20454bivhryc!xkx89$'
    )
    django.setup()
    application = get_wsgi_application()


if __name__ == "__main__":
    init_django()
    execute_from_command_line()
