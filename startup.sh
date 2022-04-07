#!/bin/bash
#python manage.py runserver 0.0.0.0:8000
python manage.py migrate
gunicorn sampleProject.asgi:application -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000