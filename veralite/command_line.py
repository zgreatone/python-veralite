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

    parser.add_argument('--ip', dest='ip',
                        help='the ip for veralite system',
                        metavar='IP',
                        required=True)

    parser.add_argument('-u', '--user', dest='user',
                        help='username for veralite',
                        metavar='USER',
                        required=True)

    parser.add_argument('-p', '--password', dest='password',
                        help='password for veralite',
                        metavar='PASSWORD',
                        required=True)

    subparsers = parser.add_subparsers(dest='command',
                                       help='command help')

    light_parser = subparsers.add_parser('light', help='light commands')

    light_subparser = light_parser.add_subparsers(dest='sub_command', help='sub command help')

    # list light devices
    list_light_parser = light_subparser.add_parser('list', help='show vera light devices')

    modify_light_parser = light_subparser.add_parser('modify', help='modify vera light state')
    modify_light_parser.add_argument('-id', '--identifier', dest='identifier', help='light identifier', required=True)
    change_group = modify_light_parser.add_mutually_exclusive_group(required=True)
    change_group.add_argument('--off', action='store_true', default=False,
                              help='to turn off light')
    change_group.add_argument('--on', action='store_true', default=False,
                              help='to turn on light')
    change_group.add_argument('--brightness', action='store_true', default=False,
                              help='to change light brightness')

    modify_light_parser.add_argument('-bl', '--brightness_level', dest='level', help='light brightness level [1 - 100] '
                                                                                     'default is 50',
                                     required=False, default=50)

    motion_parser = subparsers.add_parser('motion', help='motion sensor commands')
    motion_subparser = motion_parser.add_subparsers(dest='sub_command', help='sub command help')

    # list motion devices
    motion_subparser.add_parser('list', help='show vera motion devices')

    switch_parser = subparsers.add_parser('switch', help='switch commands')
    switch_subparser = switch_parser.add_subparsers(dest='sub_command', help='sub command help')

    # list switch devices
    switch_subparser.add_parser('list', help='show vera switch devices')

    return parser.parse_args()


def main():
    args = parse_args()

    with Veralite(args.ip, args.user, args.password) as vapi:

        if "command" not in args:
            print('command not found')
        elif args.command == "light":
            handle_light_command(args, vapi)

        elif args.command == "motion":
            # handle motion sensor command
            print("motion")
        elif args.command == "switch":
            # handle switch sensor command
            print("switch")


def handle_light_command(args, vapi):
    """
    Method to handle light commands
    :param args: command line args
    :param vapi: veralite object
    """
    dimming_lights = vapi.dimming_lights
    # handle light command
    if "sub_command" not in args or args.sub_command == "list":

        # sort by identifier
        sorted_list = sorted(dimming_lights, key=lambda key: dimming_lights[key].identifier)

        # print out values
        for value in sorted_list:
            print(dimming_lights[value])
    elif args.sub_command == "modify":
        # handle modification of light
        light_identifier = args.identifier
        if light_identifier in dimming_lights:
            light_device = vapi.dimming_lights[light_identifier]
            if args.on:
                print("turn on light")
                vapi.turn_on_dimming_light(light_device)
            elif args.off:
                print("turn off light")
                vapi.turn_off_dimming_light(light_device)
            elif args.brightness:
                print("set brightness level")
                brightness_level = args.level
                vapi.set_brightness_level_dimming_light(light_device, brightness_level)
        else:
            print("light with identifier[" + light_identifier + "] could not be found")


if __name__ == '__main__':
    main()
