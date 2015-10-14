#!/usr/bin/env python
import simplejson as json


class Scene:

    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

    def __repr__(self):
        return json.dumps({"identifier": self.identifier, "name": self.name})
