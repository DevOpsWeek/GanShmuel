#!/bin/bash
docker rm -f $(docker ps -aq)
docker build -t flaskapp .
docker run -it -p 5000:5000 flaskapp