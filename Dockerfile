FROM python:3.11

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# Project files and settings
RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y
RUN pip3 install -U pip setuptools && pip3 install pipenv

RUN mkdir /app
COPY . /app/

WORKDIR /app

RUN chmod +x /app/docker-entrypoint.sh

ARG environment=production

ENV DJANGO_SETTINGS_MODULE=ico.settings.$environment

RUN pipenv install --deploy --system

CMD gunicorn ico.core.wsgi:application --bind 0.0.0.0:80

EXPOSE 80
