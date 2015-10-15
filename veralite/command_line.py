#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
veralite.py -- a python interface to the Veralite
"""

from __future__ import print_function
import argparse
import os
import sys
import configparser

from device import Light
from veralite import Veralite


def parse_args():
    prog = os.path.basename(sys.argv[0])
    config_file = os.path.sep.join(('~', '.config', prog, 'config'))

    parser = argparse.ArgumentParser(prog=prog, add_help=False)
    parser.add_argument('--conf', default=config_file,
                        help='config file (default %s)' % config_file,
                        metavar='FILE')

    args, remaining_argv = parser.parse_known_args()

    defaults = {}
    config_file = os.path.expanduser(args.conf)
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read([config_file])

    description = 'Command line interface to Veralite™ Smart Home Controller'
    parser = argparse.ArgumentParser(description=description,
                                     parents=[parser])

    parser.set_defaults(**defaults)

    parser.add_argument('--ip', dest='ip_address',
                        help='the ip for veralite system',
                        metavar='IP',
                        required=True)

    parser.add_argument('-u', '--user', dest='user',
                        help='username for nest.com',
                        metavar='USER',
                        required=True)

    parser.add_argument('-p', '--password', dest='password',
                        help='password for nest.com',
                        metavar='PASSWORD',
                        required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    with Veralite(args.ip, args.user, args.password) as vapi:
        vapi.devices


if __name__ == '__main__':
    main()
