from django.core.management import BaseCommand
from users.models import User, UserRoles


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin = User.objects.create(
            email="user_stark@mail.com",
            first_name="Tony",
            last_name="Stark",
            role=UserRoles.ADMIN,
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        admin.set_password("stark")
        admin.save()
        print("The admin created")

        moderator = User.objects.create(
            email="moderator@mail.com",
            first_name="Jane",
            last_name="Stark",
            role=UserRoles.MODERATOR,
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )
        moderator.set_password("stark")
        moderator.save()
        print("The moderator created")

        user = User.objects.create(
            email="spongebob@mail.com",
            first_name="SpongeBob",
            last_name="SquarePants",
            role=UserRoles.USER,
            is_staff=False,
            is_active=True,
            is_superuser=False,
        )
        user.set_password("user")
        user.save()
        print("The user created")