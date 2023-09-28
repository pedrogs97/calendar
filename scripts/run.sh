#!/bin/bash

docker build . -t calendar
{ # try
    docker network create --driver=bridge main
} || { # catch
    echo "network ok"
}
docker run -d --name=calendar --net=main -p 5000:5000 calendar
