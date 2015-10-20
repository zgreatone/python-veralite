#!/usr/bin/python
"""Veralite™
   Okpe Pessu <opessu@zgreatone.net>

   Module to get interact with veralite and devices it controls
"""
import logging

from device import DimmingLight
from device import Switch
from device import MotionSensor
from scene import Scene

import utils

_DATA_ENDPOINT = '/port_3480/data_request?id=user_data'

# create logger
logger = logging.getLogger('veralite')


class Veralite(object):
    def __init__(self, ip, user=None, password=None):
        self.ip = ip
        self.user = user
        self.password = password
        self.rooms = {}
        self.dimming_lights = {}
        self.scenes = {}
        self.motion_sensors = {}
        self.switches = {}

    def __enter__(self):
        self.update_devices()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def _get_data(self):
        """
        Method gets data through http request from veralite
        :return:
        """
        logger.debug("retrieving data from veralite")

        response_content = utils.perform_get_request(self.ip, self.user, self.password, _DATA_ENDPOINT, {})

        return response_content

    def update_devices(self):
        """
        Method populates devices with their current states
        :return:
        """

        response_content = self._get_data()
        devices = response_content['devices']
        rooms = response_content['rooms']
        available_scenes = response_content['scenes']

        # handle processing rooms
        for room in rooms:
            if room["id"] not in self.rooms:
                self.rooms[int(room["id"])] = room["name"]

        # handle processing scenes
        for scene in available_scenes:
            self.scenes[str(scene["id"])] = Scene(str(str(scene["id"])), scene["name"])

        # handle processing devices
        for device in devices:
            if "device_type" in device:

                # get room name
                if "room" not in device or int(device["room"]) not in self.rooms:
                    room_name = "Room not found"
                else:
                    room_name = self.rooms[int(device["room"])]

                # motion sensor
                if "MotionSensor" in device["device_type"]:

                    self._load_sensor(device, room_name, motion=True)

                elif ("DimmableLight" in device["device_type"] in device["device_type"]) \
                        and "Sensor" not in device["device_type"]:

                    self._load_dimming_light(device, room_name)

                elif ("BinaryLight" in device["device_type"] or "WeMoControllee" in device["device_type"]) \
                        and "Sensor" not in device["device_type"]:

                    self._load_switch(device, room_name)

    def _load_dimming_light(self, device, room_name):
        """
        Utility method to create DimmingLight Device
        :param device: json object containing dimming light information
        :param room_name: the room name string
        """
        # get device state
        brightness = None
        device_state = None
        for state in device["states"]:
            if state["variable"] == "Status":
                device_state = state["value"]
            if state["variable"] == "LoadLevelStatus":
                brightness = state["value"]

        # add light to dictionary
        self.dimming_lights[int(device["id"])] = DimmingLight(int(device["id"]), device["name"], room_name,
                                                              device_state, brightness)

    def _load_switch(self, device, room_name):
        """
        Utility method to create Switch device
        :param device: json object containing switch information
        :param room_name: the room name string
        """
        # get device state
        device_state = None
        for state in device["states"]:
            if state["variable"] == "Status":
                device_state = state["value"]

        # add light to dictionary
        self.switches[int(device["id"])] = Switch(int(device["id"]), device["name"], room_name, device_state)

    def _load_sensor(self, device, room_name, motion=False):
        """
        Utility method to create Motion Sensor Device
        :param device: json object containing Motion Sensor information
        :param room_name: the room name string
        """
        configured = None
        capabilities = None
        armed = None
        # motion = False
        for state in device["states"]:
            if state["variable"] == "Armed":
                device_state = state["value"]
                armed = state["value"]
            if state["variable"] == "Capabilities":
                capabilities = state["value"]
            if state["variable"] == "Configured":
                configured = state["value"]
                # if state["variable"] == "SensorMlType":
                #     if state["value"] == "1,3,5":
                #         motion = True

        # add motion sensor to dictionary
        if motion:
            self.motion_sensors[int(device["id"])] = MotionSensor(int(device["id"]), device["name"], room_name,
                                                                  device_state, configured, capabilities, armed)

    def turn_on_dimming_light(self, device):
        """
        Turns on `veralite.device.DimmingLight`
        :param device: the `veralite.device.DimmingLight` object
        :return: returns `dict`
        """
        try:
            response = utils.update_device_state(self.ip, self.user, self.password, device, "1")
            return response
        except Exception as e:
            return {'result': False, 'message': str(e)}

    def turn_off_dimming_light(self, device):
        """
        Turns off `veralite.device.DimmingLight`
        :param device: the `veralite.device.DimmingLight` object
        :return: returns `dict`
        """
        try:
            response = utils.update_device_state(self.ip, self.user, self.password, device, "0")
            return response
        except Exception as e:
            return {'result': False, 'message': str(e)}

    def set_brightness_level_dimming_light(self, device, level):
        """
        Set the brightness level of `veralite.device.DimmingLight`
        :param device: the `veralite.device.DimmingLight` object
        :param level: the brightness level
        :return: returns `dict`
        """
        try:
            response = utils.update_brightness(self.ip, self.user, self.password, device, level)
            return response
        except Exception as e:
            return {'result': False, 'message': str(e)}

    def turn_on_switch(self, device):
        """
        Turns on `veralite.device.Switch`
        :param device: the `veralite.device.Switch` object
        :return: returns `dict`
        """
        try:
            response = utils.update_device_state(self.ip, self.user, self.password, device, "1")
            return response
        except Exception as e:
            return {'result': False, 'message': str(e)}

    def turn_off_switch(self, device):
        """
        Turns off `veralite.device.Switch`
        :param device: the `veralite.device.Switch` object
        :return: returns `dict`
        """
        try:
            response = utils.update_device_state(self.ip, self.user, self.password, device, "0")
            return response
        except Exception as e:
            return {'result': False, 'message': str(e)}

    def arm_motion_sensor(self, device):
        """
        Arms `veralite.device.MotionSensor`
        :param device: the `veralite.device.MotionSensor` object
        :return: returns `dict`
        """
        try:
            response = utils.update_sensor_state(self.ip, self.user, self.password, device, "1")
            return response
        except Exception as e:
            return {'result': False, 'message': str(e)}

    def disarm_motion_sensor(self, device):
        """
        DisArms `veralite.device.MotionSensor`
        :param device: the `veralite.device.MotionSensor` object
        :return: returns `dict`
        """
        try:
            response = utils.update_sensor_state(self.ip, self.user, self.password, device, "0")
            return response
        except Exception as e:
            return {'result': False, 'message': str(e)}
