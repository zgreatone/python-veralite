#!/usr/bin/python
"""Veralite™ Devices
   Okpe Pessu <opessu@zgreatone.net>

   Module holding device classes
"""
import simplejson as json


class Device(object):
    def __init__(self, identifier, name, room, state):
        """

        :param identifier:
        :param name:
        :param room:
        :param state:
        """
        self.identifier = identifier
        self.name = name
        self.room = room
        self.state = state

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name, "room": self.room, "state": self.state})


class Light(Device):
    def __init__(self, identifier, name, room, state):
        self.identifier = identifier
        self.name = name
        self.room = room
        self.state = state

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name, "room": self.room, "state": self.state})


class DimmingLight(Light):
    def __init__(self, identifier, name, room, state, brightness):
        self.identifier = identifier
        self.name = name
        self.room = room
        self.state = state
        self.brightness = brightness

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name, "room": self.room, "state": self.state,
                           "brightness": self.brightness})


class Switch(Light):
    def __init__(self, identifier, name, room, state):
        self.identifier = identifier
        self.name = name
        self.room = room
        self.state = state

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name, "room": self.room, "state": self.state})


class MotionSensor(Device):
    STATE_SERVICE = "urn:micasaverde-com:serviceId:SecuritySensor1"

    def __init__(self, identifier, name, room, state, configured, capabilities, armed):
        self.identifier = identifier
        self.name = name
        self.room = room
        self.state = state
        self.configured = configured
        self.capabilities = capabilities
        self.armed = armed

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name, "room": self.room, "state": self.state,
                           "configured": self.configured, "capabilities": self.capabilities, "armed": self.armed})
