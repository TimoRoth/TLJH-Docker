#!/bin/bash
set -xe
docker compose pull
docker compose build --pull
docker compose up -d
docker system prune -f
