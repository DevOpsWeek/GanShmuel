#!/bin/bash
set WEIGHT_PORT 8081
docker image rm -f weight_web:latest
docker-compose down
docker-compose up