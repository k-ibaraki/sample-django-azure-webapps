# sample-django-azure-webapps

## install

    poetry update

## 起動

    poetry run python manage.py runserver

or

    poetry run gunicorn sampleProject.asgi:application -w 2 -k uvicorn.workers.UvicornWorker
