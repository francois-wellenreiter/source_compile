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

def parent(args, params):
    logging.info("Running image : {}".format(args.image))
    os.system(args.docker + " run -it --rm --privileged" +
        " --user=" + str(os.getuid()) + ":" + str(os.getgid()) +
        " -v /var/run/docker.sock:/var/run/docker.sock" +
        " -v " + os.getcwd() + ":/src" +
        " -v " + os.path.join(os.path.dirname(os.path.abspath(__file__))) + ":/code" +
        " -v " + os.environ["HOME"] + ":/home" +
        " -e HOME=/home" +
        " -e USER=" + os.getlogin() +
        " " + args.image + 
        " python3 /code/compile.py" +
        " " + ' '.join(map(str, params)))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-d", "--docker", action = "store", type = str, default = "/usr/bin/docker")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    res = parser.parse_known_args()
    args = res[0]
    params = res[1]

    print(args, params)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    return args, params

def main():
    args, params = parse()
    parent(args, params)


if __name__ == "__main__":
    main()



