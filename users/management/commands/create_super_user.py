from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_user = User.objects.create(
            email="user_stark@mail.com",
            first_name="Tony",
            last_name="Stark",
            is_staff=True,
            is_active=True,
            is_superuser=True
        )
        admin_user.set_password("stark")
        admin_user.save()