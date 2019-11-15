#!/usr/bin/python3

import yaml
import re
import argparse
import multiprocessing as mp
import logging
import os, sys
from functools import partial
from git import Repo


IMAGE="compile:latest"
CUDA="cuda"
BASE="base"
DOCKER="_DOCKER_"

def parent(args):
    logging.info("Building image : {}-{}".format(args.image, BASE))
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__))))
    os.system(args.docker + " build . -f Dockerfile -t " + args.image + "-" + BASE + " --target " + BASE)
    logging.info("Building image : {}-{}".format(args.image, CUDA))
    os.system(args.docker + " build . -f Dockerfile -t " + args.image + "-" + CUDA + " --target " + CUDA)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-d", "--docker", action = "store", type = str, default = "/usr/bin/docker")
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



