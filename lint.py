#!/usr/bin/env python2.7

import os.path
from subprocess import check_output, CalledProcessError
from itertools import tee, izip_longest


PYLINT_HEADER_PREFIX = "*************"
SALT_REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
SALT_PACKAGE_ROOT = os.path.join(SALT_REPO_ROOT, "salt")
PYLINTRC = os.path.join(SALT_REPO_ROOT, ".pylintrc")


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..., (sN, None)"
    a, b = tee(iterable)
    next(b, None)
    return izip_longest(a, b)


def stripped(iterable):
    for line in iterable:
        yield line.strip()


def annotate_headers(iterable):
    for line in iterable:
        yield line, line.startswith(PYLINT_HEADER_PREFIX)


def dropping_kwargs_warnings(iterable):
    for line in iterable:
        if line.endswith("Unused argument 'kwargs'"):
            continue
        yield line


def dropping_bodyless_headers(iterable):
    for current, subsequent in pairwise(annotate_headers(iterable)):
        cur_line, cur_is_header = current
        next_is_header = (False if subsequent is None else subsequent[1])
        if cur_is_header and next_is_header:
            continue
        yield cur_line


with open(os.devnull) as blackhole:
    try:
        output = check_output(["pylint", "--rcfile={}".format(PYLINTRC), SALT_PACKAGE_ROOT], stderr=blackhole)
    except CalledProcessError as err:
        output = err.output

raw_lines = output.splitlines()
stripped_lines = stripped(raw_lines)
non_kwargs_lines = dropping_kwargs_warnings(stripped_lines)
interesting_lines = dropping_bodyless_headers(non_kwargs_lines)

for line in interesting_lines:
    print line
