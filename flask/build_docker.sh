#!/bin/sh

#read the enviroment variables from .env.dev
[ -e "$PWD"/.env.dev ] && . "$PWD"/.env.dev

app="hirethec-app"
docker build -t ${app} .
docker run -p 30000:5000 -d \
  --name=${app} \
  -e FLASK_DEBUG=${FLASK_DEBUG}\
  -v $PWD:/flask_app ${app}