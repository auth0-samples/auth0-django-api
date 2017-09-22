#!/usr/bin/env bash
docker build -t auth0-django-api .
docker run --env-file .env -p 8000:8000 -it auth0-django-api
