#!/usr/bin/env bash

docker network inspect bridge

docker run -ti -v $(pwd):/root/src zaquestion/sonarqube-scanner