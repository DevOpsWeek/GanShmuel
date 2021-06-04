#!/bin/sh

export BILLING_PORT=$1
export WEIGHT_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' weight-for-test_web_1)
docker-compose down
docker-compose build
docker-compose --build-arg IP=WEIGHT_IP up 
