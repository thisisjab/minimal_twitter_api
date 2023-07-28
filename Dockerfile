FROM python:3.10.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./Pipfile ./Pipfile.lock .env /code

RUN pip install pipenv

RUN pipenv install --system --deploy

COPY . /code
