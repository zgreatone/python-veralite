#!/usr/bin/python
"""Veralite™
   Okpe Pessu <opessu@zgreatone.net>

   Module to holding anything have to do with scenes.
"""
import simplejson as json


class Scene(object):
    """
    Scene object used to store information about a scene in vera
    """

    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name})
