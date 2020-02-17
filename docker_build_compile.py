#!/usr/bin/python3

import os, sys, io
import argparse
import logging
import docker
from datetime import datetime


IMAGE="compile:latest"
CUDA="cuda"
LIBC="libc"
DOCKER="_DOCKER_"
DOCKERFILE="Dockerfile"
STREAM="stream"
AUX="aux"
ID="ID"
URL="unix:/var/run/docker.sock"

def parent(args):
    cli = docker.APIClient(base_url=URL)

    logging.warning("Building image : {}-{} on {}".format(args.image, LIBC, datetime.now()))
    log = cli.build(path = os.path.join(os.path.dirname(os.path.abspath(__file__))),
        tag = args.image + "-" + LIBC,
        rm = True,
        dockerfile = DOCKERFILE,
        nocache = args.refresh,
        target = LIBC,
        use_config_proxy = True)
    for line in log:
        logging.debug("{}".format(line))
    logging.warning("Built image : {}-{} on {}".format(args.image, LIBC, datetime.now()))

    if args.cuda:
        logging.warning("Building image : {}-{} on {}".format(args.image, CUDA, datetime.now()))
        log = cli.build(path = os.path.join(os.path.dirname(os.path.abspath(__file__))),
            tag = args.image + "-" + CUDA,
            rm = True,
            dockerfile = DOCKERFILE,
            nocache = args.refresh,
            target = CUDA,
            use_config_proxy = True)
        for line in log:
            logging.debug("{}".format(line))
        logging.warning("Built image : {}-{} on {}".format(args.image, CUDA, datetime.now()))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.WARNING)
    parser.add_argument("-c", "--cuda", action = "store_true")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    parser.add_argument("-R", "--refresh", action = "store_true", default = False)
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



