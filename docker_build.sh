#!/bin/bash

docker build . -f Dockerfile -t $1 --target base 
docker build . -f Dockerfile -t $1-cuda --target cuda
