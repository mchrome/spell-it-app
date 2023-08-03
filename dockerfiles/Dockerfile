FROM python:3.10-alpine

COPY pip-requirements/requirements.txt /temp/requirements.txt
COPY spell_it_app /spell_it_app
WORKDIR /spell_it_app
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -v -r /temp/requirements.txt

RUN adduser --disabled-password default-user

USER default-user