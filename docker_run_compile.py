#!/usr/bin/python3

import os, sys, pwd
import argparse
import logging
import docker
from docker.types import LogConfig


def parent(args):
    logging.warning("Running image : {}".format(args.image))

    DOCK_SOCK="/var/run/docker.sock"
    SRC="/src"
    CODE="/code"
    HOME="/home/" + pwd.getpwuid(os.getuid()).pw_name
    USER=pwd.getpwuid(os.getuid()).pw_name
    NAME = "compile" + os.getcwd().replace('/', '_')

    cli = docker.APIClient()
    cont = cli.create_container(image = args.image,
        command = [
            *args.command,
            *args.params[1:]
        ],
        name = "compile" + os.getcwd().replace('/', '_'),
        environment = {
            "HOME" : HOME,
            "USER" : USER,
            "USERNAME" : USER,
            "LOGNAME" : USER
        },
        user = str(os.getuid()) + ":" + str(os.getgid()),
        working_dir = SRC,
        volumes = [ SRC, CODE, HOME, DOCK_SOCK ],
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
            HOME: {
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

    logging.warning("Ran image : {}".format(args.image))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-i", "--image", action = "store", type = str, default = "compile:latest-libc")
    parser.add_argument("-c", "--command", action = "store", type = str, nargs='+', default = [ "python3", "/code/compile.py" ])
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



