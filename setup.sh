#!/bin/bash

python manage.py migrate
python manage.py collectstatic
python manage.py compilemessages
python manage.py seed
python manage.py run_tasks
DJANGO_SUPERUSER_PASSWORD=changeme python manage.py createsuperuser --noinput --username admin --email admin@example.dev
