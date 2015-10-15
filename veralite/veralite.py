#!/usr/bin/python
"""Veralite™
   Okpe Pessu <opessu@zgreatone.net>
"""
import simplejson as json
import requests
import random
import logging

from requests.auth import HTTPDigestAuth

from device import Light
from device import MotionSensor
from scene import Scene

URL_ENDPOINT = '/port_3480/data_request?id=user_data'

# create logger
logger = logging.getLogger('veralite')


class Veralite:
    def __init__(self, ip, user=None, password=None):
        self.ip = ip
        self.user = user
        self.password = password
        self.rooms = {}
        self.lights = {}
        self.scenes = {}
        self.motion_sensors = {}

    def __enter__(self):
        self.update_devices()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def get_data(self):
        """
        Method gets data through http request from veralite
        :return:
        """
        logger.debug("retrieving data from veralite")
        user = self.user
        password = self.password
        ip = self.ip
        p = {'rand': random.random()}
        url = "http://" + ip + URL_ENDPOINT

        # TODO handle exception in the case of connection issues
        if user is not None and password is not None:
            response = requests.get(url,
                                    params=p,
                                    auth=HTTPDigestAuth(user, password))
        else:
            response = requests.get(url,
                                    params=p)

        response_content = json.loads(response.__dict__['_content'])

        return response_content

    def update_devices(self):
        """
        Method loads
        :return:
        """

        response_content = self.get_data()
        devices = response_content['devices']
        rooms = response_content['rooms']
        available_scenes = response_content['scenes']

        # handle processing rooms
        for room in rooms:
            if room["id"] not in self.rooms:
                self.rooms[room["id"]] = room["name"]

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

                    self.load_sensor(device, room_name, motion=True)

                elif ("Light" in device["device_type"] or "WeMoControllee" in device["device_type"]) \
                        and "Sensor" not in device["device_type"]:

                    self.load_light(device, room_name)

    def load_light(self, device, room_name):
        """

        :param device:
        :param room_name:
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
        self.lights[device["id"]] = Light(device["id"], device["name"], room_name, device_state, brightness)

    def load_sensor(self, device, room_name, motion=False):
        """

        :param device:
        :param room_name:
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
            self.motion_sensors[device["id"]] = MotionSensor(device["id"],
                                                             device["name"],
                                                             room_name,
                                                             device_state,
                                                             configured,
                                                             capabilities,
                                                             armed)
