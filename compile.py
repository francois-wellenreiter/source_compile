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

def clone(k, v, args):
    logging.info("Cloning " + k)
    if not os.path.exists(os.path.join(args.target, v[DIR])):
        Repo.clone_from(v[URL], os.path.join(args.target, v[DIR]), branch = v[BRANCH])

def update(k, v, args):
    logging.info("Updating " + k)
    repo = Repo(os.path.join(args.target, v[DIR]))
    repo.remotes.origin.pull()
    repo.submodule_update(recursive = True)

def clean(k, v, args):
    logging.info("Cleaning " + k)
    os.chdir(os.path.join(args.target, v[DIR]))
    if CLEAN in v:
        for cmd in v[CLEAN]:
            logging.info("Executing " + cmd)
            os.system(cmd)

def build(k, v, args):
    logging.info("Building " + k)
    os.chdir(os.path.join(args.target, v[DIR]))
    if BUILD in v:
        for cmd in v[BUILD]:
            logging.info("Executing " + cmd)
            os.system(cmd)

def worker(data, args):
    for k, v in data.items():
        if v[ENABLED]:
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
                        print("Error ", exc, "while loading ", f)
                        exit(0)


def parent(args):
    with mp.Pool(processes = args.parallelize) as pool:
        pool.map(partial(worker, args = args), load_files(args.dir))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("-d", "--dir", action = "store", default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yml"))
    parser.add_argument("-t", "--target", action = "store", default = os.path.join(os.getenv("HOME"), "src"))
    parser.add_argument("-c", "--clean", action = "store_true")
    parser.add_argument("-b", "--build", action = "store_true")
    parser.add_argument("-u", "--update", action = "store_true")
    parser.add_argument("-C", "--cores", action = "store", type = int, default = 1)
    parser.add_argument("-P", "--parallelize", action = "store", type = int, default = 1)
    args = parser.parse_args()

    logger = mp.log_to_stderr()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        logging.basicConfig(level=logging.INFO)

    if args.parallelize > 0:
        os.putenv("__CORE_NB__", str(args.cores))
        os.putenv("__MVN_OPTS__", "--global-settings /code/maven_settings.xml -T " + str(args.cores))
        os.putenv("__SBT_OPTS__", "-Dsbt.global.base=/home/.sbt -Dsbt.ivy.home=/home/.ivy2")

    return args


def main():
    parent(parse())

if __name__ == "__main__":
    main()
