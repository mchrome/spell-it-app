FROM python:3.10-alpine

COPY requirements.txt /temp/requirements.txt
COPY spell_it_app /spell_it_app
WORKDIR /spell_it_app
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password default-user

USER default-user