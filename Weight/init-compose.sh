#!/bin/bash
set WEIGHT_PORT $1
docker image rm -f weight_web:latest
docker-compose down
docker-compose --env-file ./.env.stg up