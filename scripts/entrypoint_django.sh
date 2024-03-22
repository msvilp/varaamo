#!/bin/sh

if [ -z "$IN_DEVCONTAINER" ]; then
    # Not in the dev container, exit the script
    exit 0
fi

pipenv run python manage.py runserver 0.0.0.0:8000
