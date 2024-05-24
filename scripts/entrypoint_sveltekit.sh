#!/bin/sh

if [ -z "$IN_DEVCONTAINER" ]; then
    # Not in the dev container, exit the script
    exit 0
fi

# Define the path to the file you are waiting for
FILE_PATH="/tmp/npm_installed"

# Loop until the file exists
while [ ! -f "$FILE_PATH" ]; do
  echo "Waiting for $FILE_PATH to exist..."
  sleep 10 # Wait for 10 second before checking again
done

echo "$FILE_PATH exists. Continuing execution..."

cd varaamo-frontend
npm run dev -- --host 0.0.0.0
