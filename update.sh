#!/bin/bash
cd "$(dirname "$0")"
set -xe

if ! [[ -d config ]]; then
	mkdir config
	cp tljh/config.yaml config
	mkdir -p config/templates/extra-assets
	mkdir -p config/jupyterhub_config.d
fi

docker compose pull
docker compose build --pull
docker compose up -d
docker system prune -f
