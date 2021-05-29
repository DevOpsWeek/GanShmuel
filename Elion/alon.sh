#!/bin/bash


docker rm -f $( docker ps -aq )
docker build -t test .
docker run -it test bash -c "python app.py" 
