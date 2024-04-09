#!/bin/sh

if [ -z "$IN_DEVCONTAINER" ]; then
    # Not in the dev container, exit the script
    exit
fi

cd varaamo-frontend
npm run dev -- --host 0.0.0.0
