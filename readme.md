# The PetPlace platform includes sections:

- Breeds
- Dogs
- Users
- Reviews

### This project uses the .venv virtual environment.

After setting up the virtual environment, install dependencies from the requirements.txt file

```bash
pip install -r requirements.txt
```

### Creating database:

1) Fill the .env file according to the .env_sample file
2) Create database using command:

```bash
python manage.py create_database
```

### Creating migrations:

1) python manage.py makemigrations
2) python manage.py migrate

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### Create users using the command:

```bash
python manage.py create_super_user
```

### Populating the database with fixtures:

```bash
python manage.py loaddata dogs.json
```

### Run the command to start the Redis server:
(Run on another terminal)

```bash
redis-server
```

### Run the command to start the PetPlace app:
(Run on another terminal)

```bash
python manage.py runserver
```