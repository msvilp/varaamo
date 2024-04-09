#!/bin/bash

# Wait for the database container to be ready
until nc -z -v -w30 db 3306
do
  echo "Waiting for database container to be ready..."
  # Wait for 5 seconds before checking again
  sleep 5
done

exec "$@"
