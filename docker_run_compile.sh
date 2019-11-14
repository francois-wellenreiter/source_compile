#!/bin/bash

DOCKER=${DOCKER:-"/usr/bin/docker"}

TOOLS=${TOOLS:-$( dirname $( realpath $0 ))}

export __MVN_OPTS__="--global-settings /code/maven_settings.xml" 
export __SBT_OPTS__="-Dsbt.global.base=/home/.sbt -Dsbt.ivy.home=/home/.ivy2"

$DOCKER run \
    -it \
    --rm \
    -m 2G \
    --privileged \
    --ipc=host \
    -v $PWD:/work \
    -v $TOOLS:/code \
    -v $HOME:/home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e USER=$USER \
    -e HOME=/home \
    -e __MVN_OPTS__ \
    -e __SBT_OPTS__ \
    --user=`id -u`:`id -g` \
    $@

