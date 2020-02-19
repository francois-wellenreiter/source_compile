#!/usr/bin/python3

import os, sys
import docker
import argparse
import logging

IMAGE="compile:latest-libc"
PYTHON="python3"
BASE_CMD="/code/compile.py"
DOCKER_SOCK="unix://var/run/docker.sock"
SRC="/src"
CODE="/code"
ROOT="/root"
TMP_ROOT="/tmp/root"
FORMAT = '%(asctime)-15s - %(message)s'

def parent(args):
    logging.warning("Running image : {}".format(args.image))

    if not os.path.isdir(TMP_ROOT):
       os.mkdir(TMP_ROOT)

    cli = docker.from_env()
    cont = cli.containers.run(image = args.image,
        command = [
            PYTHON,
            BASE_CMD,
            *args.params[1:]
        ],
        mounts = [
            docker.types.Mount(source = TMP_ROOT, target = ROOT, type = "bind"),
            docker.types.Mount(source = os.getcwd(), target = SRC, type = "bind"),
            docker.types.Mount(source = os.path.join(os.path.dirname(os.path.abspath(__file__))), target = CODE, type = "bind"),
            ],
        working_dir = SRC,
        detach = True,
        use_config_proxy  = True,
        auto_remove = True)

    for line in cont.logs(stream = True):
        logging.warning("{}".format(line.strip()))

    logging.warning("Ran image : {}".format(args.image))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.WARNING)
    parser.add_argument("params", nargs = argparse.REMAINDER)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format = FORMAT)
    else:
        logging.basicConfig(level=args.loglevel, format = FORMAT)

    return args

def main():
    args = parse()
    parent(args)


if __name__ == "__main__":
    main()



