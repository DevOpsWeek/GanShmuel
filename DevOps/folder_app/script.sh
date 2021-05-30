#!/bin/bash
git checkout --track origin/$1
cd $1
docker compose up .
