#!/bin/sh
export WEIGHT_PORT=$1
echo $WEIGHT_PORT
docker image rm weight_web:latest
docker-compose down
docker-compose up
