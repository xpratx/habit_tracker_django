from django.apps import AppConfig
import os


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habit_tracker.users'

    def ready(self):
        
        import habit_tracker.users.signals

        
        if os.environ.get("CREATE_SUPERUSER") == "True":
            from django.contrib.auth import get_user_model
            User = get_user_model()

            username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
            email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

            if username and password and not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
