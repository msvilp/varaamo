FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    # Required for installing/upgrading pip packages like mysqlclient etc.:
    libc-dev gcc make python3-dev mariadb-dev jpeg-dev zlib-dev

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies into a virtualenv
RUN pip install --upgrade pipenv

COPY ./Pipfile .
COPY ./Pipfile.lock .
COPY ./setup.py .
RUN mkdir varaamo
COPY ./varaamo/__init__.py ./varaamo/
COPY ./myapps/__init__.py ./myapps/
COPY ./manage.py .

RUN pipenv install --dev --deploy

# Copy project code
COPY . /code/