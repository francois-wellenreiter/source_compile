#!/usr/bin/python3

import argparse
import multiprocessing as mp
import logging
import os, sys


IMAGE="compile:latest-libc"

def parent(args):
    logging.info("Running image : {}".format(args.image))
    logging.debug("{} run -it --rm --privileged"
        " -v /var/run/docker.sock:/var/run/docker.sock"
        " -v {}:/src"
        " -v {}:/code"
        " -v /tmp/root:/root"
        " {} python3 /code/compile.py {}"
        .format(args.docker, os.getcwd(),
        os.path.join(os.path.dirname(os.path.abspath(__file__))),
        args.image,
        ' '.join(map(str, args.params[1:]))))
    try:
        os.system(args.docker + " run -it --rm --privileged"
          " -v /var/run/docker.sock:/var/run/docker.sock"
          " -v " + os.getcwd() + ":/src"
          " -v " + os.path.join(os.path.dirname(os.path.abspath(__file__))) + ":/code"
          " -v /tmp/root:/root"
          " " + args.image +
          " python3 /code/compile.py" +
          " -l " + str(args.loglevel) +
          (" -v" if args.verbose else "") +
          " " + ' '.join(map(str, args.params[1:])))
    except Exception as err:
        logging.error("calling {} failed, err {}", args.docker, err)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-d", "--docker", action = "store", type = str, default = "/usr/bin/docker")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.ERROR)
    parser.add_argument("params", nargs=argparse.REMAINDER)
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



