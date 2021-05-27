#!/bin/sh
docker rm -f $(docker ps -aq)
docker build -t test .
docker run -it -p 5001:5001 test 
