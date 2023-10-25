FROM python:3.9-slim-buster

WORKDIR /app

LABEL maintainer='ebodesilone@gmail.com'
LABEL description='Code pour django et celery'

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#RUN apt-get update \
#  && apt-get install -y build-essential \
#  && apt-get install -y libpq-dev \
#  && apt-get install -y gettext \
#  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

ENTRYPOINT ["/entrypoint"]