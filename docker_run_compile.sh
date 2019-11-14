#!/bin/bash

DOCKER=${DOCKER:-"/usr/bin/docker"}

TOOLS=`dirname $0`

CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    -it \
    --rm \
    -m 2G \
    --privileged
    --ipc=host \
    -v $PWD:/work \
    -v $TOOLS:/code \
    -v $HOME:/home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e USER=$USER \
    -e HOME=/home \
    -e __MVN_OPTS__="--global-settings /code/maven_settings.xml" \
    -e __SBT_OPTS__="-Dsbt.global.base=/home/.sbt -Dsbt.ivy.home=/home/.ivy2" \
    --user=`id -u`:`id -g` \
    "

$DOCKER run -it $CMDLINE_DOCKER_RUN $@
