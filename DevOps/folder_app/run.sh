#!/bin/bash
docker rm $(docker ps -aq)
docker rmi $(docker images)
docker build -t app_image .
docker run -it -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 app_image
