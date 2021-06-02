#!/bin/sh

set BILLING_PORT=$1
docker-compose down
docker-compose --env-file ./.env.stg up 