#!/usr/bin/python3

import os, sys
import docker
import argparse
import logging
from datetime import datetime


IMAGE="compile:latest-libc"
PYTHON="python3"
BASE_CMD="/code/compile.py"
DOCKER_SOCK="unix://var/run/docker.sock"
SOCK="/var/run/docker.sock"
SRC="/src"
CODE="/code"
ROOT="/root"
TMP_ROOT="/tmp/root"

def parent(args):
    logging.info("Running image : {} on {}".format(args.image, datetime.now()))

    try:
        cli = docker.from_env()
        cont = cli.containers.run(image = args.image,
            command = [
                PYTHON,
                BASE_CMD,
                *args.params[1:]
                ],
            mounts = [ 
                docker.types.Mount(source = SOCK, target = SOCK, type = "bind"),
                docker.types.Mount(source = TMP_ROOT, target = ROOT, type = "bind"),
                docker.types.Mount(source = os.getcwd(), target = SRC, type = "bind"),
                docker.types.Mount(source = os.path.join(os.path.dirname(os.path.abspath(__file__))), target = CODE, type = "bind"),
            ],
            working_dir = SRC,
            auto_remove = True,
            detach = True)

    except Exception as err:
        logging.error("calling {} failed, err {}", args.image, err)

    for line in cont.logs(stream=True):
        print(line.strip())

    logging.info("Ran image : {} on {}".format(args.image, datetime.now()))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.ERROR)
    parser.add_argument("params", nargs = argparse.REMAINDER)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=args.loglevel)

    return args

def main():
    args = parse()
    parent(args)


if __name__ == "__main__":
    main()



