#!/bin/bash
docker image rm -f weight_web:latest
docker-compose down
docker-compose up