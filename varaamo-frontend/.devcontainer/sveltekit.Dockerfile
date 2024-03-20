FROM mcr.microsoft.com/devcontainers/typescript-node:0-18

RUN mkdir -p /workspace/varaamo-frontend

WORKDIR /workspace

COPY ./varaamo-frontend/package*.json ./varaamo-frontend

RUN cd /workspace/varaamo-frontend; npm install

COPY . ./

WORKDIR /workspace/varaamo-frontend
