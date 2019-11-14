#!/usr/bin/python3

import yaml
import re
import argparse
import multiprocessing as mp
import logging
import os, sys
from functools import partial
from git import Repo

DIR="dir"
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
        logging.debug( 'Downloading {} : ( {} )\r'.format(key, message))
    else:
        logging.debug( '{} for {}: ( {} )\r'.format(fn.__name__, key, message))



def clone(k, v, args):
    logging.info("Cloning {}".format(k))

    if not os.path.exists(os.path.join(args.directory, v[DIR])):
        try:
            repo = Repo.clone_from(v[URL], os.path.join(args.directory, v[DIR]), branch = v[BRANCH], progress = partial(progress, fn = Repo.clone_from, key = k))
        except Exception as err:
            logging.warning("Error when cloning {}, {}".format(k ,err))
        try:
            repo.submodule_update(recursive = True, init = True, progress = partial(progress, fn = repo.submodule_update, key = k))
        except Exception as err:
            logging.warning("Error when updating submodules for {}, {}".format(k ,err))



def update(k, v, args):
    if args.update:
        logging.info("Updating {}".format(k))
    
        try:
            repo = Repo(os.path.join(args.directory, v[DIR]))
        except Exception as err:
            logging.warning("Error no repository found for {}, {}".format(k ,err))

        if args.clean:
            try:
                repo.head.reset(index=True, working_tree=True)
            except Exception as err:
                logging.warning("Error when resetting {}, {}".format(k ,err))
    
            try:
                repo.git.gc()
            except Exception as err:
                logging.warning("Error when compressing git repository {}, {}".format(k ,err))
    
    
        try:
            repo.remotes.origin.pull(progress = partial(progress, fn = repo.remotes.origin.pull, key = k))
        except Exception as err:
            logging.warning("Error when pulling {}, {}".format(k ,err))
    
        try:
            repo.submodule_update(recursive = True, init = True, progress = partial(progress, fn = repo.submodule_update, key = k))
        except Exception as err:
            logging.warning("Error when updating submodules for {}, {}".format(k ,err))



def clean(k, v, args):
    if args.clean:
        logging.info("Cleaning {}".format(k))
        os.chdir(os.path.join(args.directory, v[DIR]))
        if CLEAN in v:
            for cmd in v[CLEAN]:
                logging.debug("Executing clean {}".format(k))
                os.system(cmd)



def build(k, v, args):
    if args.build:
        logging.info("Building {}".format(k))
        os.chdir(os.path.join(args.directory, v[DIR]))
        if BUILD in v:
            for cmd in v[BUILD]:
                logging.debug("Executing build {}".format(cmd))
                os.system(cmd)



def worker(data, args):
    for k, v in data.items():
        if args.target is None or k in args.target:
            if v[ENABLED]:
                clone(k, v ,args)
                update(k, v, args)
                clean(k, v, args)
                build(k, v, args)



def load_files(dir):
    for dirpath, dnames, fnames in os.walk(dir):
        for f in fnames:
            if f.endswith(".yml"):
                with open(os.path.join(dirpath, f), 'r') as h:
                    try:
                        yield yaml.safe_load(h)
                    except yaml.YAMLError as exc:
                        print("Error ", exc, "while loading ", f)
                        exit(0)




def parent(args):
    with mp.Pool(processes = args.parallelize) as pool:
        pool.map(partial(worker, args = args), load_files(args.configuration))




def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-c", "--configuration", action = "store", default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yml"))
    parser.add_argument("-d", "--directory", action = "store", default = "/src")
    parser.add_argument("-t", "--target", action = "store", nargs="+")
    parser.add_argument("-C", "--clean", action = "store_true")
    parser.add_argument("-B", "--build", action = "store_true")
    parser.add_argument("-U", "--update", action = "store_true")
    parser.add_argument("-p", "--procs", action = "store", type = int, default = 1)
    parser.add_argument("-P", "--parallelize", action = "store", type = int, default = 1)
    args = parser.parse_args()

    logger = mp.log_to_stderr()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        logging.basicConfig(level=logging.INFO)

    if args.procs > 0:
        os.putenv(PROCS, str(args.procs))

        if MVNOPTS in os.environ:
            os.putenv(MVNOPTS, os.environ[MVNOPTS] + " -T " + str(args.procs))
        else:
            os.putenv(MVNOPTS, "-T " + str(args.procs))

        if SBTOPTS in os.environ:
            os.putenv(SBTOPTS, os.environ[SBTOPTS])

    return args




def main():
    parent(parse())

if __name__ == "__main__":
    main()



