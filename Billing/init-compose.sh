#!/bin/sh

export BILLING_PORT=$1
docker-compose down
docker-compose up 
