#!/usr/bin/python3

import argparse
import logging
import os, sys


IMAGE="compile:latest"
CUDA="cuda"
LIBC="libc"
DOCKER="_DOCKER_"

def parent(args):
    logging.info("Building image : {}-{}".format(args.image, LIBC))
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__))))
    logging.debug("{} build . --rm -f Dockerfile -t {}-{} --target {})".format(args.docker, args.image, LIBC, LIBC))
    os.system(args.docker + " build . --rm -f Dockerfile -t " + args.image + "-" + LIBC + " --target " + LIBC)
    if args.cuda:
        logging.info("Building image : {}-{}".format(args.image, CUDA))
        logging.debug("{} build . --rm -f Dockerfile -t {}-{} --target {})".format(args.docker, args.image, CUDA, CUDA))
        os.system(args.docker + " build . --rm -f Dockerfile -t " + args.image + "-" + CUDA + " --target " + CUDA)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-c", "--cuda", action = "store_true")
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



