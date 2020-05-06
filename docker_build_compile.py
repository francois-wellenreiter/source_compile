#!/usr/bin/python3

import os, sys, io
import argparse
import logging
import docker

IMAGE="compile:latest"
LIBC="libc"
DOCKERFILE="Dockerfile"
STREAM="stream"
AUX="aux"
ID="ID"
FORMAT = '%(asctime)-15s - %(message)s'

def parent(args):
    cli = docker.APIClient()

    logging.warning("Building image : {}-{}".format(args.image, LIBC))
    log = cli.build(path = os.path.join(os.path.dirname(os.path.abspath(__file__))),
        tag = args.image + "-" + LIBC,
        rm = True,
        dockerfile = DOCKERFILE,
        nocache = args.refresh,
        target = LIBC)
    for line in log:
        logging.debug("{}".format(line))
    logging.warning("Built image : {}-{}".format(args.image, LIBC))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.WARNING)
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    parser.add_argument("-R", "--refresh", action = "store_true", default = False)
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



