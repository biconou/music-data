#!/bin/bash

export HOSTNAME=`hostname`

docker-compose --env-file .env.${HOSTNAME} down -v

docker-compose --env-file .env.${HOSTNAME} up -d --build

