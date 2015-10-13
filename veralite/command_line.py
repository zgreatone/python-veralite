#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
veralite.py -- a python interface to the Veralite
"""

from __future__ import print_function
import argparse
import os
import sys

from . import device
from . import utils


def parse_args():
    prog = os.path.basename(sys.argv[0])
    config_file = os.path.sep.join(('~', '.config', prog, 'config'))

    parser = argparse.ArgumentParser(prog=prog, add_help=False)
    parser.add_argument('--conf', default=config_file,
                        help='config file (default %s)' % config_file,
                        metavar='FILE')


def main():
    args = parse_args()

if __name__ == '__main__':
    main()