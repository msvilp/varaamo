#!/bin/sh

# This is a script that will be run after the devcontainer is created.
# In local dev, we don't need to include dependencies in the docker image, so
# we install them after the container is created.
# Since the workspace is mounted from the host, the dependencies will be stored
# on the host machine and don't need to be reinstalled every time.

echo "Running post create script"
GITURL=$(grep -A1 '\[remote "origin"\]' /tmp/gitconfig | tail -1 | sed -E 's/^.+url.=.//')
[ ! -d "/path/to/dir" ] && echo "cloning $GITURL" && git clone $GITURL /tmp/code && mv -f /tmp/code/* /tmp/code/.[!.]* /code/

echo "Installing pip dependencies"
export PIPENV_VENV_IN_PROJECT=1
pipenv install --dev
touch /tmp/pipenv_installed

echo "Installing npm dependencies"
cd varaamo-frontend
pnpm install
touch /tmp/npm_installed
