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


def setenv(buildargs = None):

    if buildargs is None:
        buildargs = dict()

    if "DOCKER_REGISTRY" in os.environ:
       buildargs["DOCKER_REGISTRY"] = os.environ["DOCKER_REGISTRY"]

    if "HTTP_PROXY" in os.environ:
       buildargs["HTTP_PROXY"] = os.environ["HTTP_PROXY"]

    if "HTTPS_PROXY" in os.environ:
       buildargs["HTTPS_PROXY"] = os.environ["HTTPS_PROXY"]

    if "FTP_PROXY" in os.environ:
       buildargs["FTP_PROXY"] = os.environ["FTP_PROXY"]

    if "NO_PROXY" in os.environ:
       buildargs["NO_PROXY"] = os.environ["NO_PROXY"]

    if "http_proxy" in os.environ:
       buildargs["http_proxy"] = os.environ["http_proxy"]

    if "https_proxy" in os.environ:
       buildargs["https_proxy"] = os.environ["https_proxy"]

    if "ftp_proxy" in os.environ:
       buildargs["ftp_proxy"] = os.environ["ftp_proxy"]

    if "no_proxy" in os.environ:
       buildargs["no_proxy"] = os.environ["no_proxy"]

    return buildargs


def parent(args):
    cli = docker.APIClient()

    buildargs = setenv()

    logging.warning("Building image : {}".format(args.image))
    log = cli.build(path = os.path.join(os.path.dirname(os.path.abspath(__file__))),
        tag = args.image,
        rm = True,
        buildargs = buildargs,
        dockerfile = DOCKERFILE,
        nocache = args.refresh,
        pull = args.refresh,
        target = LIBC)
    for line in log:
        logging.debug("{}".format(line))
    logging.warning("Built image : {}".format(args.image))


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



