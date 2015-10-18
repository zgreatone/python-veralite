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
    light_subparser.add_parser('list', help='show vera light devices')

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

    # motion sensor subparser setup ###
    motion_parser = subparsers.add_parser('motion', help='motion sensor commands')
    motion_subparser = motion_parser.add_subparsers(dest='sub_command', help='sub command help')

    # list motion devices
    motion_subparser.add_parser('list', help='show vera motion sensor devices')

    modify_motion_parser = motion_subparser.add_parser('modify', help='modify motion sensor state')
    modify_motion_parser.add_argument('-id', '--identifier', dest='identifier', help='motion sensor identifier',
                                      required=True)
    motion_change_group = modify_motion_parser.add_mutually_exclusive_group(required=True)
    motion_change_group.add_argument('--disarm', action='store_true', default=False,
                                     help='to disarm sensor')
    motion_change_group.add_argument('--arm', action='store_true', default=False,
                                     help='to arm sensor')

    # switch subparser setup ####
    switch_parser = subparsers.add_parser('switch', help='switch commands')
    switch_subparser = switch_parser.add_subparsers(dest='sub_command', help='sub command help')

    # list switch devices
    switch_subparser.add_parser('list', help='show vera switch devices')

    modify_switch_parser = switch_subparser.add_parser('modify', help='modify vera switch state')
    modify_switch_parser.add_argument('-id', '--identifier', dest='identifier', help='switch identifier', required=True)
    switch_change_group = modify_switch_parser.add_mutually_exclusive_group(required=True)
    switch_change_group.add_argument('--off', action='store_true', default=False,
                                     help='to turn off switch')
    switch_change_group.add_argument('--on', action='store_true', default=False,
                                     help='to turn on switch')

    return parser.parse_args()


def main():
    args = parse_args()

    with Veralite(args.ip, args.user, args.password) as vapi:

        if "command" not in args:
            print('command not found')
        elif args.command == "light":
            # handle light command
            handle_light_command(args, vapi)

        elif args.command == "motion":
            # handle motion sensor command
            handle_motion_sensor_command(args, vapi)
        elif args.command == "switch":
            # handle switch sensor command
            handle_switch_command(args, vapi)


def handle_light_command(args, vapi):
    """
    Method to handle light commands
    :param args: command line args
    :param vapi: veralite object
    """
    dimming_lights = vapi.dimming_lights
    # handle light command
    if "sub_command" not in args or args.sub_command is None or args.sub_command == "list":

        header = "Dimming Lights"

        list_devices(header, dimming_lights)

    elif args.sub_command == "modify":
        # handle modification of light
        light_identifier = int(args.identifier)
        if light_identifier in dimming_lights:
            light_device = dimming_lights[light_identifier]
            if args.on:
                print("\t" + "Turning ON Light Device[" + light_device.name + "]")
                response = vapi.turn_on_dimming_light(light_device)
                if response['result']:
                    print("\t\tResponse: OK")
                else:
                    print("\t\tResponse: BAD, Reason[" + response.message + "]")
            elif args.off:
                print("\t" + "Turning OFF Light Device[" + light_device.name + "]")
                response = vapi.turn_off_dimming_light(light_device)
                if response['result']:
                    print("\t\tResponse: OK")
                else:
                    print("\t\tResponse: BAD, Reason[" + response.message + "]")
            elif args.brightness:
                brightness_level = args.level
                print("\t" + "Setting Brightness Level of Light Device[" + light_device.name +
                      "] to [" + brightness_level + "]")
                response = vapi.set_brightness_level_dimming_light(light_device, brightness_level)

                # handle response
                if response['result']:
                    print("\t\tResponse: OK")
                else:
                    print("\t\tResponse: BAD, Reason[" + response.message + "]")
        else:
            print("\tNo Switch Device found with id[" + str(light_identifier) + "]")


def handle_switch_command(args, vapi):
    """
    Method to handle switch commands
    :param args: command line args
    :param vapi: veralite object
    """
    switches = vapi.switches
    # handle switch command
    if "sub_command" not in args or args.sub_command is None or args.sub_command == "list":
        header = "Switches"

        list_devices(header, switches)
    elif args.sub_command == "modify":
        # handle modification of switch
        switch_identifier = int(args.identifier)
        if switch_identifier in switches:
            switch_device = switches[switch_identifier]
            if args.on:
                print("\t" + "Turning ON Switch Device[" + switch_device.name + "]")
                response = vapi.turn_on_switch(switch_device)
                if response['result']:
                    print("\t\tResponse: OK")
                else:
                    print("\t\tResponse: BAD, Reason[" + response.message + "]")
            elif args.off:
                print("\t" + "Turning OFF Switch Device[" + switch_device.name + "]")
                response = vapi.turn_off_switch(switch_device)
                if response['result']:
                    print("\t\tResponse: OK")
                else:
                    print("\t\tResponse: BAD, Reason[" + response.message + "]")
        else:
            print("\tNo Switch Device found with id[" + str(switch_identifier) + "]")


def handle_motion_sensor_command(args, vapi):
    """
    Method to handle motion sensors commands
    :param args: command line args
    :param vapi: veralite object
    """
    motion_sensors = vapi.motion_sensors
    # handle motion sensor command
    if "sub_command" not in args or args.sub_command is None or args.sub_command == "list":
        header = "Motion Sensors"

        list_devices(header, motion_sensors)
    elif args.sub_command == "modify":
        # handle modification of motion sensors
        motion_sensor_identifier = int(args.identifier)
        if motion_sensor_identifier in motion_sensors:
            motion_sensor_device = motion_sensors[motion_sensor_identifier]
            if args.arm:
                print("\t" + "Arming Motion Sensor Device[" + motion_sensor_device.name + "]")
                response = vapi.arm_motion_sensor(motion_sensor_device)
                if response['result']:
                    print("\t\tResponse: OK")
                else:
                    print("\t\tResponse: BAD, Reason[" + response.message + "]")
            elif args.disarm:
                print("\t" + "DisArming Motion Sensor Device[" + motion_sensor_device.name + "]")
                response = vapi.disarm_motion_sensor(motion_sensor_device)
                if response['result']:
                    print("\t\tResponse: OK")
                else:
                    print("\t\tResponse: BAD, Reason[" + response.message + "]")
        else:
            print("\tNo Motion Sensor Device found with id[" + str(motion_sensor_identifier) + "]")


def list_devices(header, devices):
    # sort by identifier
    sorted_list = sorted(devices, key=lambda key: devices[key].identifier)
    print("\t" + header + ":")
    # print out values
    for value in sorted_list:
        print("\t\tID:[" + str(devices[value].identifier) + "]  Name:[" + devices[value].name + "]")


if __name__ == '__main__':
    main()
