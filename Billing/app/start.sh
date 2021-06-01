#!/bin/bash
while ! nc -z db 5000; do sleep 3; done
python app.py
