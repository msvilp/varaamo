FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# This is a singlar container for local development
# It contains both django and nodejs environment

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/); \
    echo "arch: $arch"; \
    if [ "$arch" = "arm64" ]; then echo "libz1" > archpackages.txt; else echo "lib32z1-dev" > archpackages.txt; fi;

# Install nodejs
RUN node_version=v20.8.0; arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/x64/); cd /opt \
 && curl -LO https://nodejs.org/dist/${node_version}/node-${node_version}-linux-${arch}.tar.xz \
 && tar xJf node-${node_version}-linux-${arch}.tar.xz \
 && rm node-${node_version}-linux-${arch}.tar.xz \
 && ln -s /opt/node-${node_version}-linux-${arch}/bin/node /usr/bin/node \
 && ln -s /opt/node-${node_version}-linux-${arch}/bin/npm /usr/bin/npm \
 && ln -s /opt/node-${node_version}-linux-${arch}/bin/npx /usr/bin/npx \
 && ln -s /opt/node-${node_version}-linux-${arch}/bin/corepack /usr/bin/corepack

# install yarn and pnpm
RUN corepack enable && corepack prepare yarn@stable --activate

# Set work directory
RUN mkdir /code && chown vscode:vscode /code
WORKDIR /code

COPY ./.devcontainer /tmp/.devcontainer

# Save git config to get correct remote url
COPY ./.git/config /tmp/gitconfig

# Install pipenv
RUN pip install --upgrade pipenv

