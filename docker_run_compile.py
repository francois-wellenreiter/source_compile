#!/usr/bin/python3

import os, sys, pwd, grp
import argparse
import logging
import docker
from docker.types import LogConfig

IMAGE="compile:latest"
CPU="cpu"
CMD=[ "python3", "/code/compile.py" ]


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
    logging.warning("Running image : {}".format(args.image + "-" + args.flavour))

    DOCK_SOCK="/var/run/docker.sock"
    DOCK_GROUP="docker"
    SRC="/src"
    CODE="/code"
    USER=pwd.getpwuid(os.getuid()).pw_name
    HOME="/home/" + USER
    NAME = "compile" + os.getcwd().replace('/', '_')

    env = {
        "HOME" : HOME,
        "USER" : USER,
        "USERNAME" : USER,
        "LOGNAME" : USER
    }

    env = setenv(env)

    cli = docker.APIClient()
    cont = cli.create_container(image = args.image + "-" + args.flavour,
        command = [
            *args.command,
            *args.params[1:]
        ],
        name = "compile" + os.getcwd().replace('/', '_'),
        environment = env,
        user = str(os.getuid()) + ":" + str(grp.getgrnam(DOCK_GROUP).gr_gid),
        working_dir = SRC,
        volumes = [ SRC, CODE, HOME, DOCK_SOCK ],
        runtime = args.runtime,
        host_config = cli.create_host_config(
          auto_remove = True,
          binds={
            os.getcwd(): {
              'bind': SRC,
              'mode': 'rw',
            },
            os.path.join(os.path.dirname(os.path.abspath(__file__))): {
              'bind': CODE,
              'mode': 'rw',
            },
            os.environ["HOME"]: {
              'bind': HOME,
              'mode': 'rw',
            },
            DOCK_SOCK: {
              'bind': DOCK_SOCK,
              'mode': 'rw',
            }
          }
        ),
        detach = False,
        stdin_open = True,
    )

    cli.start(container=NAME)
    for line in cli.logs(NAME, stream = True, stdout = True,
stderr = True, follow = True, timestamps = False, tail = "all"):
      logging.warning("{}".format(line))

    logging.warning("Ran image : {}".format(args.image + "-" + args.flavour))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-i", "--image", action = "store", type = str, default
= IMAGE)
    parser.add_argument("-f", "--flavour", action = "store", type = str,
default = CPU)
    parser.add_argument("-c", "--command", action = "store", type = str,
nargs='+', default = CMD)
    parser.add_argument("-r", "--runtime", action = "store", type = str, default = None)
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.WARNING)
    parser.add_argument("params", nargs = argparse.REMAINDER)
    args = parser.parse_args()

    FORMAT='%(asctime)-15s - %(message)s'
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



