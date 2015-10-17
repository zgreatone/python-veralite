#!/usr/bin/python
# -*- coding:utf-8 -*-

# Native modules
import os
import unittest
import json
from unittest.mock import MagicMock

# Custom modules
from veralite import veralite


class TestVeralite(unittest.TestCase):
    def setUp(self):
        self.ip = "0.0.0.0"
        self.user = "user"
        self.password = "password"
        self.veralite = veralite.Veralite(self.ip, self.user, self.password)
        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "test_vera_output.json")
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            self.veralite.get_data = MagicMock(return_value=data)

    def test_update_device(self):
        self.veralite.update_devices()

        switches = self.veralite.switches
        self.assertEquals(7, len(switches))

        dimming_lights = self.veralite.dimming_lights
        self.assertEquals(10, len(dimming_lights))

        motion_sensors = self.veralite.motion_sensors
        self.assertEquals(3, len(motion_sensors))


if __name__ == '__main__':
    unittest.main()
