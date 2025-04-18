from django.core.management import BaseCommand
import pyodbc
from config.settings import USER, PASSWORD, HOST, DATABASE, PAD_DATABASE, DRIVER


class Command(BaseCommand):
    def handle(self, *args, **options):
        connection_string = f"""DRIVER={DRIVER};
                                SERVER={HOST};
                                DATABASE={PAD_DATABASE};
                                 USER={USER};
                                PASSWORD={PASSWORD};
                                Trusted_Connection=yes;"""

        try:
            conn = pyodbc.connect(connection_string)
        except pyodbc.ProgrammingError as e:
            print(e)
        else:
            conn.autocommit = True
            try:
                conn.execute(fr"CREATE DATABASE {DATABASE}")
            except pyodbc.ProgrammingError as e:
                print(e)
            else:
                print(f"Database {DATABASE} created")


