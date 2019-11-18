#!/usr/bin/python3

import argparse
import multiprocessing as mp
import logging
import os, sys


IMAGE="compile:latest-base"

def parent(args, params):
    logging.info("Running image : {}".format(args.image))
    logging.debug("{} run -it --rm --privileged" 
        " --user={}:{}"
        " -v /var/run/docker.sock:/var/run/docker.sock"
        " -v {}:/src"
        " -v {}:/code"
        " -v {}:/home"
        " -e HOME=/home"
        " -e USER={}"
        " {} python3 /code/compile.py{} {}"
        .format(args.docker, str(os.getuid()), str(os.getgid()), os.getcwd(), 
        os.path.join(os.path.dirname(os.path.abspath(__file__))), os.environ["HOME"], 
        os.getlogin(), args.image, 
        " -v" if args.verbose else "", ' '.join(map(str, params))))
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
        (" -v" if args.verbose else "") +
        " " + ' '.join(map(str, params)))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-d", "--docker", action = "store", type = str, default = "/usr/bin/docker")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    args, params = parser.parse_known_args()

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



