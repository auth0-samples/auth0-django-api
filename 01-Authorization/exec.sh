#!/usr/bin/env bash
docker build -t auth0-django-api .
docker run --env-file .env -p 3010:3010 -it auth0-django-api
