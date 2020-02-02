#!/usr/bin/python3

import os, sys
import argparse
import logging
import docker
from datetime import datetime


IMAGE="compile:latest"
CUDA="cuda"
LIBC="libc"
DOCKER="_DOCKER_"
DOCKERFILE="Dockerfile"

def parent(args):
    cli = docker.from_env()

    print("Building image : {}-{} on {}".format(args.image, LIBC, datetime.now()))
    bld = cli.images.build(path = os.path.join(os.path.dirname(os.path.abspath(__file__))),
        tag = args.image + "-" + LIBC,
        rm = True,
        dockerfile = DOCKERFILE,
        target = LIBC)
    print("Built image : {}-{} on {}".format(args.image, LIBC, datetime.now()))

    if args.cuda:
        print("Building image : {}-{} on {}".format(args.image, CUDA, datetime.now()))
        bld = cli.images.build(path = os.path.join(os.path.dirname(os.path.abspath(__file__))),
            tag = args.image + "-" + CUDA,
            rm = True,
            dockerfile = DOCKERFILE,
            target = CUDA)
        print("Built image : {}-{} on {}".format(args.image, CUDA, datetime.now()))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-c", "--cuda", action = "store_true")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    return args

def main():
    args = parse()
    parent(args)


if __name__ == "__main__":
    main()



