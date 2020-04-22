#!/usr/bin/python3

from functools import partial
import multiprocessing as mp
import os, sys
import argparse
import yaml
from git import Repo
import logging

FORMAT = '%(asctime)-15s %(product)s - %(message)s'
ENABLED="enabled"
URL="url"
BRANCH="branch"
CLEAN="clean"
BUILD="build"
FORCE="force"

PROCS="__PROCS__"
SBTOPTS="__SBT_OPTS__"
MVNOPTS="__MVN_OPTS__"


def progress(op_code, cur_count, max_count=None, message='', fn = None, key = ""):
    d = { "product": key }
    if fn is None:
        logging.debug( 'Downloading : ( {} / {} )\r'.format(cur_count, max_count, message), extra = d)
    else:
        logging.debug( '{} : ( {} / {} ) {}\r'.format(fn.__name__, cur_count, max_count, message), extra = d)



def clone(k, v, args):
    d = { "product": k}
    logging.info("Cloning", extra = d)
    try:
        repo = Repo.clone_from(v[URL], os.path.join(args.directory, k), branch = v[BRANCH], progress = partial(progress, fn = Repo.clone_from, key = k))
    except Exception as err:
        logging.error("Error when cloning {}".format(err), extra = d)
        return
    try:
        repo.submodule_update(recursive = True, init = True)
    except Exception as err:
        logging.debug("No submodules to update {}".format(err), extra = d)
    logging.info("Cloned", extra = d)



def update(k, v, args):
    d = { "product": k}
    logging.info("Updating", extra = d)
    try:
        repo = Repo(os.path.join(args.directory, k))
    except Exception as err:
        logging.error("Error no repository found {}".format(err), extra = d)
        return
    if args.clean:
        try:
            repo.head.reset(index=True, working_tree=True)
        except Exception as err:
            logging.error("Error when resetting {}".format(err), extra = d)

        try:
            repo.git.gc()
        except Exception as err:
            logging.error("Error when compressing git repository {}".format(err), extra = d)
    try:
        repo.remotes.origin.pull(progress = partial(progress, fn = repo.remotes.origin.pull, key = k))
    except Exception as err:
        logging.error("Error when pulling {}".format(err), extra = d)
    try:
        repo.submodule_update(recursive = True, init = True)
    except Exception as err:
        logging.debug("No submodules to update {}".format(err), extra = d)
    logging.info("Updated", extra = d)



def clean(k, v, args):
    d = { "product": k}
    logging.info("Cleaning", extra = d)
    os.chdir(os.path.join(args.directory, k))
    if CLEAN in v:
        for cmd in v[CLEAN]:
            logging.debug("Executing {}".format(cmd), extra = d)
            os.system(cmd)
    logging.info("Cleaned", extra = d)


def build(k, v, args):
    d = { "product": k}
    logging.info("Building", extra = d)
    os.chdir(os.path.join(args.directory, k))
    if BUILD in v:
        for cmd in v[BUILD]:
            logging.debug("Executing {}".format(cmd), extra = d)
            os.system(cmd)
    logging.info("Built", extra = d)


def worker(data, args):
    for k, v in data.items():
        d = { "product": k}
        if args.target is None or k in args.target:
            if v[ENABLED] or args.force:
                logging.info("Managing", extra = d)
                if not os.path.exists(os.path.join(args.directory, k)):
                    clone(k, v ,args)
                if args.update:
                    update(k, v, args)
                if args.clean:
                    clean(k, v, args)
                if args.build:
                    build(k, v, args)
                logging.info("Managed", extra = d)



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
        print("{}\t{}\t{}".format("+->" if ENABLED in v and v[ENABLED] else "|\t\t\t", k, v[URL]))


def parent(args):
    if args.list:
        print_list(args)
    else:
        with mp.Pool(processes = args.parallelize) as pool:
            res = pool.map(partial(worker, args = args), load_files(args.configuration))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-l", "--loglevel", action = "store", type = int, default = logging.INFO)
    parser.add_argument("-c", "--configuration", action = "store", type=str, default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yml"))
    parser.add_argument("-d", "--directory", action = "store", type=str, default = os.getcwd())
    parser.add_argument("-t", "--target", action = "store", type=str, nargs="+")
    parser.add_argument("-f", "--force", action = "store_true")
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
        logging.basicConfig(level=logging.DEBUG, format = FORMAT)
    else:
        logger.setLevel(args.loglevel)
        logging.basicConfig(level=args.loglevel, format = FORMAT)

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



