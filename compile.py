#!/usr/bin/python3

import argparse
from functools import partial
import os, sys
import subprocess
import multiprocessing as mp
import logging
from git import Repo
import yaml, json
import networkx as nx

# specific pattern
YML_EXT=".yml"
ENABLED="enabled"
URL="url"
BRANCH="branch"
CLEAN="clean"
BUILD="build"
DEPS="deps"
INFO="info"

# git specific pattern
ORIGIN="origin"

# cloc specific pattern
HEADER="header"
NFILES="nFiles"
BLANK="blank"
COMMENT="comment"
CODE="code"
SUM="SUM"

# compilation specific pattern
PROCS="__PROCS__"
SBTOPTS="__SBT_OPTS__"
MVNOPTS="__MVN_OPTS__"


def progress(op_code, cur_count, max_count=None, message='', fn = None, key = ""):
    if fn is None:
        logging.debug( 'Downloading -\t{} : ( {} / {} ) {}\r'.format(key, cur_count, max_count, message))
    else:
        logging.debug( 'Downloading -\t{} : {} - ( {} / {} ) {}\r'.format(key, fn.__name__, cur_count, max_count, message))
    return



def clone(k, v, args):
    logging.info("Cloning -\t{}".format(k))
    try:
        repo = Repo.clone_from(v[URL], os.path.join(args.directory, k),
            branch = v[BRANCH], progress = partial(progress, fn = Repo.clone_from, key = k))
    except Exception as err:
        logging.error("Error when cloning {} with {}".format(k, err))
        return
    try:
        repo.submodule_update(recursive = True, init = True)
    except Exception as err:
        logging.debug("No submodules {} to update {}".format(k, err))
    logging.info("Cloned -\t{}".format(k))
    return



def update(k, v, args):
    logging.info("Updating -\t{}".format(k))
    try:
        repo = Repo(os.path.join(args.directory, k))
        origin = repo.remotes[ORIGIN]
        origin.fetch(progress = partial(progress, fn = origin.fetch, key = k))
        repo.heads.master.set_tracking_branch(origin.refs.master)
    except Exception as err:
        logging.error("Error no repository {} found {}".format(k, err))
        return
    if args.clean:
        try:
            repo.head.reset(index=True, working_tree=True)
        except Exception as err:
            logging.error("Error when resetting {} {}".format(k, err))

        try:
            repo.git.gc()
        except Exception as err:
            logging.error("Error when compressing git repository {} with {}".format(k, err))
    try:
        repo.remotes.origin.pull(progress = partial(progress, fn = repo.remotes.origin.pull, key = k))
    except Exception as err:
        logging.error("Error when pulling {} with {}".format(k, err))
    try:
        repo.submodule_update(recursive = True, init = True)
    except Exception as err:
        logging.debug("No submodules to update {} with {}".format(k, err))
    logging.info("Updated -\t{}".format(k))
    return


def clean(k, v, args):
    logging.info("Cleaning -\t{}".format(k))
    os.chdir(os.path.join(args.directory, k))
    if CLEAN in v:
        for cmd in v[CLEAN]:
            logging.debug("Executing -\t {} - {}".format(k, cmd))
            os.system(cmd)
    logging.info("Cleaned -\t{}".format(k))
    return


def build(k, v, args):
    logging.info("Building -\t{}".format(k))
    os.chdir(os.path.join(args.directory, k))
    if BUILD in v:
        for cmd in v[BUILD]:
            logging.debug("Executing -\t {} - {}".format(k, cmd))
            os.system(cmd)
    logging.info("Built -\t{}".format(k))
    return


#######################################


def worker(args, in_q, out_q):
    while True:
        k, v = in_q.get()
        if k is None:
            return

        if args.target is None or k in args.target:
            if (ENABLED in v and v[ENABLED]) or args.force:
                logging.info("Managing -\t{}".format(k))
                if not os.path.exists(os.path.join(args.directory, k)):
                    clone(k, v ,args)
                if args.update:
                    update(k, v, args)
                if args.clean:
                    clean(k, v, args)
                if args.build:
                    build(k, v, args)
                logging.info("Managed -\t{}".format(k))
            else:
                logging.info("Managing -\t{}\t- DISABLED".format(k))

        out_q.put(k)


def start_workers(args, deps):
    on_hold = []
    working = []
    in_q = mp.Queue()
    out_q = mp.Queue()

    for num in range(args.parallelize):
        mp.Process(target = worker, args = (args, in_q, out_q)).start()

    while len(deps) > 0:
        # get leaves of the graph and add them if they are not managed yet 
        for k in deps.nodes():
            if deps.out_degree(k) == 0 and k not in on_hold and k not in working:
                on_hold += [k]

        for k in on_hold:
            in_q.put((k, deps.nodes[k]))
            working += [k]
            on_hold.remove(k)

        k = out_q.get()
        deps.remove_node(k)
        working.remove(k)

    for num in range(args.parallelize):
        in_q.put((None, None))
    return


#######################################


def fill_graph(deps, d):
    for k, v in d.items():
        deps.add_node(k, **v)
        if DEPS in v:
            for dep in v[DEPS]:
                deps.add_node(dep)
                deps.add_edge(k, dep)
    if not nx.is_directed_acyclic_graph(deps):
        raise TypeError
    return


def parse_files(dir):
    deps = nx.DiGraph()
    for dirpath, dnames, fnames in os.walk(dir):
        for f in fnames:
            if f.endswith(YML_EXT):
                with open(os.path.join(dirpath, f), 'r') as h:
                    try:
                        fill_graph(deps, yaml.safe_load(h))
                    except (TypeError, yaml.YAMLError) as exc:
                        logging.info("Error {} while loading {}".format(exc, f))
    return deps


def print_stats(args, deps):
    for k, v in sorted(deps.nodes(data = True)):
        if ENABLED in v and v[ENABLED]:
            if os.path.exists(os.path.join(args.directory, k)):
                print("+--->\t{}".format(k))
                try:
                    out, err = subprocess.Popen(["/usr/bin/cloc", "--json", k],
                        stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
                    d = json.loads(out)
                except Exception as err:
                    logging.error("Error when reading {} output with {}".format(k, err))
                    return

                for k_, v_ in sorted(d.items()):
                    if k_ != HEADER and k_ != SUM:
                        print("|\t{} files -\t{} lines -\t{}".format(v_[NFILES], v_[CODE], k_))
                print("|\t{} files -\t{} lines -\t{}".format(d[SUM][NFILES], d[SUM][CODE], SUM))
            else:
                print("+---/\t{}".format(k))
        else:
            print("|\t{}".format(k))
    return


def print_list(deps):
    for k, v in sorted(deps.nodes(data = True)):
        print("{}\t{}".format("+--->" if ENABLED in v and v[ENABLED] else "|", k))
    return


#######################################


def parse_args():
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


#######################################


def main():
    args = parse_args()
    deps = parse_files(args.configuration)
    if args.list:
        print_list(deps)
    elif args.stats:
        print_stats(args, deps)
    else:
        start_workers(args, deps)
    return


if __name__ == "__main__":
    main()



