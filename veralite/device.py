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

    def get_state(self):
        return self.state

    def get_identifier(self):
        return self.identifier

    def update_state(self, state):
        self.state = state
