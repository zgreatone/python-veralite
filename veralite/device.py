#!/usr/bin/python
"""Veralite™ Devices
   Okpe Pessu <opessu@zgreatone.net>
"""
import simplejson as json


class Device:
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


class DimmingLight(Device):
    def __init__(self, identifier, name, room, state, brightness):
        self.identifier = identifier
        self.name = name
        self.room = room
        self.state = state
        self.brightness = brightness

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name, "room": self.room, "state": self.state,
                           "brightness": self.brightness})


class Switch(Device):
    def __init__(self, identifier, name, room, state):
        self.identifier = identifier
        self.name = name
        self.room = room
        self.state = state

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name, "room": self.room, "state": self.state})


class MotionSensor(Device):
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
