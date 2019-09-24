#!/bin/bash

DOCKER=${DOCKER:-"/usr/bin/docker"}

TOOLS=`dirname $0`

CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    --rm \
    --privileged
    --ipc=host \
    -v $PWD:/work \
    -v $TOOLS:/code \
    -v $HOME:/home \
    -v $HOME/.m2:/.m2 \
    -v $HOME/.cache:/.cache \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e USER=$USER \
    -e HOME=/home \
    --user=`id -u`:`id -g` \
    "

if [ a$MEM != a ]
then
CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    -m $MEM \
    "
fi

if [ a$CPUSET != a ]
then
CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    --cpuset-cpus=$CPUSET \
    "
fi

if [ a$PROCS != a ]
then
CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    -e PROCS=$PROCS \
    "
fi

if [ a$PARALL != a ]
then
CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    -e PARALL=$PARALL \
    "
fi

if [ a$DONT_COMPILE != a ]
then
CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    -e DONT_COMPILE=$DONT_COMPILE \
    "
fi
if [ a$DO_CLEAN != a ]
then
CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    -e DO_CLEAN=$DO_CLEAN \
    "
fi

if [ a$DONT_GATHER != a ]
then
CMDLINE_DOCKER_RUN="$CMDLINE_DOCKER_RUN \
    -e DONT_GATHER=$DONT_GATHER \
    "
fi

if [ a$DO_LOG = a -o a$DO_LOG = a0 ]
then
exec $DOCKER run -it $CMDLINE_DOCKER_RUN \
    $@
else
exec $DOCKER run -t $CMDLINE_DOCKER_RUN \
    $@ \
    | tee $HOME/docker_run_`date '+%Y-%m-%d_%H-%M-%S'`.log
fi
