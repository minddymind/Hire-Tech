#!/bin/sh

#read the enviroment variables from 
[ -e "$PWD"/.env ] && . "$PWD"/.env

app="hirethec-app"
docker build -t ${app} .
docker run -p 8000:8000 -d \
  --name=${app} \
  -e FLASK_DEBUG=${FLASK_DEBUG}\
  -v $PWD:/flask_app ${app}