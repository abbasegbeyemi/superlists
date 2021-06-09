FROM python:3.8.5-alpine

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

# install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . .