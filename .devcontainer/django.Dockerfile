FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

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
RUN mkdir myapps
COPY ./myapps/__init__.py ./myapps/
COPY ./manage.py .

RUN pipenv install --dev --deploy --system

# Copy project code
COPY . /code/
