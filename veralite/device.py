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
    def __init__(self, identifier, name, room, state, brightness):
        self.brightness = brightness
        super(Light, self).__init__(identifier, name, room, state)

    def __repr__(self):
        value = super(Light, self).__repr__()
        value["brightness"] = self.brightness
        return json.dumps(value)


class MotionSensor(Device):
    def __init__(self, identifier, name, room, state, configured, capabilities, armed):
        self.configured = configured
        self.capabilities = capabilities
        self.armed = armed
        super(MotionSensor, self).__init__(identifier, name, room, state)

    def __repr__(self):
        value = super(MotionSensor, self).__repr__()
        value["armed"] = self.armed
        value["configured"] = self.configured
        value["capabilities"] = self.capabilities
        return json.dumps(value)
