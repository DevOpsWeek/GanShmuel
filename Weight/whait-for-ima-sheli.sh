#!/bin/bash
while ! mysqladmin ping -h "db" -p "3306" ; do
    echo "Waiting for MySQL to be up..."
    sleep 1
done