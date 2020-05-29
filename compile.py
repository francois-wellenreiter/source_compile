#!/usr/bin/python3

from functools import partial
import subprocess
import multiprocessing as mp
import os, sys
import argparse
import yaml
from git import Repo
import logging

ENABLED="enabled"
URL="url"
BRANCH="branch"
CLEAN="clean"
BUILD="build"

ORIGIN="origin"

PROCS="__PROCS__"
SBTOPTS="__SBT_OPTS__"
MVNOPTS="__MVN_OPTS__"


def progress(op_code, cur_count, max_count=None, message='', fn = None, key = ""):
    if fn is None:
        logging.debug( '{} - Downloading : ( {} / {} ) {}\r'.format(key, cur_count, max_count, message))
    else:
        logging.debug( '{} - {} : ( {} / {} ) {}\r'.format(key, fn.__name__, cur_count, max_count, message))



def clone(k, v, args):
    logging.info("{} - Cloning".format(k))
    try:
        repo = Repo.clone_from(v[URL], os.path.join(args.directory, k), branch = v[BRANCH], progress = partial(progress, fn = Repo.clone_from, key = k))
    except Exception as err:
        logging.error("{} - Error when cloning {}".format(k, err))
        return
    try:
        repo.submodule_update(recursive = True, init = True)
    except Exception as err:
        logging.debug("{} - No submodules to update {}".format(k, err))
    logging.info("{} - Cloned".format(k))



def update(k, v, args):
    logging.info("{} - Updating".format(k))
    try:
        repo = Repo(os.path.join(args.directory, k))
        origin = repo.remotes[ORIGIN]
        origin.fetch(progress = partial(progress, fn = origin.fetch, key = k))
        repo.heads.master.set_tracking_branch(origin.refs.master)
    except Exception as err:
        logging.error("{} - Error no repository found {}".format(k, err))
        return
    if args.clean:
        try:
            repo.head.reset(index=True, working_tree=True)
        except Exception as err:
            logging.error("{} - Error when resetting {}".format(k, err))

        try:
            repo.git.gc()
        except Exception as err:
            logging.error("{} - Error when compressing git repository {}".format(k, err))
    try:
        repo.remotes.origin.pull(progress = partial(progress, fn = repo.remotes.origin.pull, key = k))
    except Exception as err:
        logging.error("{} - Error when pulling {}".format(k, err))
    try:
        repo.submodule_update(recursive = True, init = True)
    except Exception as err:
        logging.debug("{} - No submodules to update {}".format(k, err))
    logging.info("{} - Updated".format(k))



def clean(k, v, args):
    logging.info("{} - Cleaning".format(k))
    os.chdir(os.path.join(args.directory, k))
    if CLEAN in v:
        for cmd in v[CLEAN]:
            logging.debug("{} - Executing {}".format(k, cmd))
            os.system(cmd)
    logging.info("{} - Cleaned".format(k))


def build(k, v, args):
    logging.info("{} - Building".format(k))
    os.chdir(os.path.join(args.directory, k))
    if BUILD in v:
        for cmd in v[BUILD]:
            logging.debug("{} - Executing {}".format(k, cmd))
            os.system(cmd)
    logging.info("{} - Built".format(k))


def worker(data, args):
    for k, v in data.items():
        if args.target is None or k in args.target:
            if v[ENABLED] or args.force:
                logging.info("{} - Managing".format(k))
                if not os.path.exists(os.path.join(args.directory, k)):
                    clone(k, v ,args)
                if args.update:
                    update(k, v, args)
                if args.clean:
                    clean(k, v, args)
                if args.build:
                    build(k, v, args)
                logging.info("{} - Managed".format(k))



def load_files(dir):
    for dirpath, dnames, fnames in os.walk(dir):
        for f in fnames:
            if f.endswith(".yml"):
                with open(os.path.join(dirpath, f), 'r') as h:
                    try:
                        yield yaml.safe_load(h)
                    except yaml.YAMLError as exc:
                        logging.info("{} - Error {} while loading {}".format(k, exc, f))


def print_stats(args):
    for d in load_files(args.configuration):
        for k, v in sorted(d.items()):
            if ENABLED in v and v[ENABLED]:
                print("+-> {}".format(k))
                subprocess.call(["/usr/bin/cloc", "--git", k])

    
def print_list(args):
    for d in load_files(args.configuration):
        for k, v in sorted(d.items()):
            print("{}\t{}\t{}".format("+->" if ENABLED in v and v[ENABLED] else "|\t\t\t", k, v[URL]))


def parent(args):
    if args.list:
        print_list(args)
    if args.stats:
        print_stats(args)
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
    parser.add_argument("-S", "--stats", action = "store_true")
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



