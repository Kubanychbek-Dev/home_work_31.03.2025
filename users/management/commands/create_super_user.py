from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_user = User.objects.create(
            email="user@mail.com",
            first_name="Spongebob",
            last_name="Squerpants",
            is_staff=True,
            is_active=True,
            is_superuser=True
        )
        admin_user.set_password("user")
        admin_user.save()