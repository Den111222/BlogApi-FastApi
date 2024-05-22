#!/usr/bin/env bash
set -e

# postgres 5432
while ! nc -z $1 $2; do
      echo "--- checking connection to $1:$2 ---"
      sleep 1
done

echo "--- ALEMBIC: UPDATING DB SCHEME ---"
cd src
alembic upgrade head
cd ../

echo "--- START GUNICORN ---"
python3 -m gunicorn --name async_auth -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000 main:app
