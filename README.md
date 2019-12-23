# Top 100 German Verbs

A simple Django web app inspired by websites such as [Verbix](https://www.verbix.com/languages/german.html) and [Reverso](http://conjugator.reverso.net/conjugation-german.html) that displays conjugation tables for the 100 most frequently used German verbs.

## Visit Website
The web app is deployed at the following Heroku site:
https://top-100-german-verbs.herokuapp.com

## Installation
Clone the project, install the dependencies, and create a virtual environment
```bash
git clone https://github.com/pres220/top-100-german-verbs.git
cd top-100-german-verbs
pipenv install
pipenv shell
```

Generate a secret key value for settings.py
```bash
DJANGO_SECRET_KEY=$(python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())')
```

Export the secret key as an environment variable
```bash
echo "export DJANGO_SECRET_KEY='$DJANGO_SECRET_KEY'" > .env
source .env
```

Migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```

Load the fixture containing the verb data
```bash
python manage.py loaddata conjugator.json
```

## Run
```bash
python manage.py runserver
```
Open browser and visit http://127.0.0.1:8000

## Test
```bash
python manage.py test
```


