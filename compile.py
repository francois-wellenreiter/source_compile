#!/usr/bin/python3

import yaml
import argparse
import multiprocessing as mp
import logging
import os, sys
from functools import partial
from git import Repo

ENABLED="enabled"
URL="url"
BRANCH="branch"
CLEAN="clean"
BUILD="build"

PROCS="__PROCS__"
SBTOPTS="__SBT_OPTS__"
MVNOPTS="__MVN_OPTS__"



def progress(op_code, cur_count, max_count=None, message='', fn = None, key = ""):
    if fn is None:
        logging.debug( 'Downloading {} : ( {} / {} )\r'.format(key, cur_count, max_count, message))
    else:
        logging.debug( '{} for {}: ( {} / {} ) {}\r'.format(fn.__name__, key, cur_count, max_count, message))



def clone(k, v, args):
    logging.info("Cloning {}".format(k))
    if not os.path.exists(os.path.join(args.directory, k)):
        try:
            repo = Repo.clone_from(v[URL], os.path.join(args.directory, k), branch = v[BRANCH], progress = partial(progress, fn = Repo.clone_from, key = k))
        except Exception as err:
            logging.error("Error when cloning {}, {}".format(k ,err))
        try:
            repo.submodule_update(recursive = True, init = True, progress = partial(progress, fn = repo.submodule_update, key = k))
        except Exception as err:
            logging.debug("Error when updating submodules for {}, {}".format(k ,err))



def update(k, v, args):
    logging.info("Updating {}".format(k))
    os.chdir(os.path.join(args.directory, k))

    try:
        repo = Repo(os.path.join(args.directory, k))
    except Exception as err:
        logging.error("Error no repository found for {}, {}".format(k ,err))

    if args.clean:
        try:
            repo.head.reset(index=True, working_tree=True)
        except Exception as err:
            logging.error("Error when resetting {}, {}".format(k ,err))

        try:
            repo.git.gc()
        except Exception as err:
            logging.error("Error when compressing git repository {}, {}".format(k ,err))


    try:
        repo.remotes.origin.pull(progress = partial(progress, fn = repo.remotes.origin.pull, key = k))
    except Exception as err:
        logging.error("Error when pulling {}, {}".format(k ,err))

    try:
        repo.submodule_update(recursive = True, init = True, progress = partial(progress, fn = repo.submodule_update, key = k))
    except Exception as err:
        logging.debug("Error when updating submodules for {}, {}".format(k ,err))



def clean(k, v, args):
    logging.info("Cleaning {}".format(k))
    os.chdir(os.path.join(args.directory, k))
    if CLEAN in v:
        for cmd in v[CLEAN]:
            logging.debug("Executing clean {}".format(k))
            os.system(cmd)



def build(k, v, args):
    logging.info("Building {}".format(k))
    os.chdir(os.path.join(args.directory, k))
    if BUILD in v:
        for cmd in v[BUILD]:
            logging.debug("Executing build {}".format(cmd))
            os.system(cmd)



def worker(data, args):
    for k, v in data.items():
        if args.target is None or k in args.target:
            if v[ENABLED]:
                print("Managing {}".format(k))
                clone(k, v ,args)
                if args.update:
                    update(k, v, args)
                if args.clean:
                    clean(k, v, args)
                if args.build:
                    build(k, v, args)



def load_files(dir):
    for dirpath, dnames, fnames in os.walk(dir):
        for f in fnames:
            if f.endswith(".yml"):
                with open(os.path.join(dirpath, f), 'r') as h:
                    try:
                        yield yaml.safe_load(h)
                    except yaml.YAMLError as exc:
                        logging.info("Error {} while loading {}".format(exc, f))
                        exit(0)


def print_list(args):
    sd = dict()
    for d in load_files(args.configuration):
        sd.update(d)

    for k, v in sorted(sd.items()):
        print("{} {}\t{}".format("+" if ENABLED in v and v[ENABLED] else "X", k, v[URL]))


def parent(args):
    if args.list:
        print_list(args)
    else:
        with mp.Pool(processes = args.parallelize) as pool:
            res = pool.map(partial(worker, args = args), load_files(args.configuration))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.ERROR)
    parser.add_argument("-c", "--configuration", action = "store", default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yml"))
    parser.add_argument("-d", "--directory", action = "store", default = os.getcwd())
    parser.add_argument("-t", "--target", action = "store", nargs="+")
    parser.add_argument("-C", "--clean", action = "store_true")
    parser.add_argument("-B", "--build", action = "store_true")
    parser.add_argument("-U", "--update", action = "store_true")
    parser.add_argument("-p", "--procs", action = "store", type = int, default = 1)
    parser.add_argument("-P", "--parallelize", action = "store", type = int, default = 1)
    parser.add_argument("-L", "--list", action = "store_true")
    args = parser.parse_args()

    logger = mp.log_to_stderr()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
    else:
        logger.setLevel(args.loglevel)
        logging.basicConfig(level=args.loglevel)

    if args.procs > 0:
        os.environ[PROCS] = str(args.procs)

        if MVNOPTS in os.environ:
            os.environ[MVNOPTS] = os.environ[MVNOPTS] + " -T " + str(args.procs)
        else:
            os.environ[MVNOPTS] = "-T " + str(args.procs)

    return args




def main():
    parent(parse())

if __name__ == "__main__":
    main()



