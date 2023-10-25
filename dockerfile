FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install --upgrade pip

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt





EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]