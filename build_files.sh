#!/usr/bin/env bash
# install dependencies
pip install -r requirements.txt

# migrate database
python manage.py makemigrations
python manage.py migrate

# collect static files
python manage.py collectstatic --noinput
