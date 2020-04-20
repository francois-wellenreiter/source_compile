#!/usr/bin/python3

import os, sys
import argparse
import logging
import docker
from docker.types import LogConfig

IMAGE="compile:latest-libc"
BASE_CMD=[ "python3", "/code/compile.py" ]
SRC="/src"
CODE="/code"
ROOT="/root"
TMP_ROOT="/tmp/root"
FORMAT = '%(asctime)-15s - %(message)s'

def parent(args):
    logging.warning("Running image : {}".format(args.image))

    if not os.path.isdir(TMP_ROOT):
       os.mkdir(TMP_ROOT)

    cli = docker.APIClient()
    cont = cli.create_container(image = args.image,
        command = [
            *args.command,
            *args.params[1:]
        ],
        volumes = [ ROOT, SRC, CODE ],
        host_config = cli.create_host_config(
          auto_remove = True,
          binds={
            ROOT: {
              'bind': TMP_ROOT,
              'mode': 'rw',
            },
            SRC: {
              'bind': os.getcwd(),
              'mode': 'rw',
            },
            CODE: {
              'bind': os.path.join(os.path.dirname(os.path.abspath(__file__))),
              'mode': 'rw',
            }
          } 
        ),
        working_dir = SRC,
        detach = False,
        stdin_open = True,
        tty = True)

    cli.start(container=cont.get('Id'))
    for line in cli.logs(container=cont.get('Id'), stream = True, stdout =
True, stderr = True):
      print(line)
   
    logging.warning("Ran image : {}".format(args.image))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-i", "--image", action = "store", type = str, default = IMAGE)
    parser.add_argument("-c", "--command", action = "store", type = str, nargs='+', default = BASE_CMD)
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.WARNING)
    parser.add_argument("params", nargs = argparse.REMAINDER)
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



