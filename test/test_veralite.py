#!/usr/bin/python
# -*- coding:utf-8 -*-

# Native modules
import os
import unittest
import json
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

# Custom modules
from veralite import exceptions
from veralite import veralite

_NUM_SWITCHES = 7
_NUM_LIGHTS = 10
_NUM_MOTION_SENSORS = 3

_RESPONSE_STRING = '{ "u:SetTargetResponse": { "JobID": "15585" } }'


class TestVeralite(unittest.TestCase):
    def setUp(self):
        self.ip = "0.0.0.0"
        self.user = "user"
        self.password = "password"
        self.veralite = veralite.Veralite(self.ip, self.user, self.password)
        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "test_vera_output.json")
        with open(json_file_path) as json_file:
            self.json_data = json.load(json_file)
            self.veralite._get_data = MagicMock(return_value=self.json_data)

    @patch('veralite.veralite.utils')
    def test_get_data(self, mock_utils):
        mock_utils.perform_get_request.return_value = self.json_data
        with veralite.Veralite(self.ip, self.user, self.password) as vapi:
            self.assertEqual(_NUM_SWITCHES, len(vapi.switches))

        self.assertTrue(mock_utils.perform_get_request.called, "update device method not present")

    def test_update_device(self):
        self.veralite.update_devices()

        switches = self.veralite.switches
        self.assertEqual(_NUM_SWITCHES, len(switches))

        dimming_lights = self.veralite.dimming_lights
        self.assertEqual(_NUM_LIGHTS, len(dimming_lights))

        motion_sensors = self.veralite.motion_sensors
        self.assertEqual(_NUM_MOTION_SENSORS, len(motion_sensors))

    @patch('veralite.veralite.utils')
    def test_turn_on_dimming_light(self, mock_utils):
        self.veralite.update_devices()
        data = json.loads(_RESPONSE_STRING)
        mock_utils.update_device_state.return_value = {'result': True, 'message': data}

        response = self.veralite.turn_on_dimming_light(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], True)

        mock_utils.update_device_state.side_effect = exceptions.InvalidDeviceError('mock test error')

        response = self.veralite.turn_on_dimming_light(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], False)

    @patch('veralite.veralite.utils')
    def test_turn_off_dimming_light(self, mock_utils):
        self.veralite.update_devices()
        data = json.loads(_RESPONSE_STRING)
        mock_utils.update_device_state.return_value = {'result': True, 'message': data}

        response = self.veralite.turn_off_dimming_light(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], True)

        mock_utils.update_device_state.side_effect = exceptions.InvalidDeviceError('mock test error')

        response = self.veralite.turn_off_dimming_light(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], False)

    @patch('veralite.veralite.utils')
    def test_set_brightness_level_dimming_light(self, mock_utils):
        self.veralite.update_devices()
        data = json.loads(_RESPONSE_STRING)
        mock_utils.update_brightness.return_value = {'result': True, 'message': data}

        response = self.veralite.set_brightness_level_dimming_light(self.veralite.switches[4], 10)

        self.assertTrue(mock_utils.update_brightness.called, "update device method not present")
        self.assertEqual(response['result'], True)

        mock_utils.update_brightness.side_effect = exceptions.InvalidDeviceError('mock test error')

        response = self.veralite.set_brightness_level_dimming_light(self.veralite.switches[4], 10)

        self.assertTrue(mock_utils.update_brightness.called, "update device method not present")
        self.assertEqual(response['result'], False)

    @patch('veralite.veralite.utils')
    def test_turn_on_switch(self, mock_utils):
        self.veralite.update_devices()
        data = json.loads(_RESPONSE_STRING)
        mock_utils.update_device_state.return_value = {'result': True, 'message': data}

        response = self.veralite.turn_on_switch(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], True)

        mock_utils.update_device_state.side_effect = exceptions.InvalidDeviceError('mock test error')

        response = self.veralite.turn_on_switch(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], False)

    @patch('veralite.veralite.utils')
    def test_turn_off_switch(self, mock_utils):
        self.veralite.update_devices()
        data = json.loads(_RESPONSE_STRING)
        mock_utils.update_device_state.return_value = {'result': True, 'message': data}

        response = self.veralite.turn_off_switch(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], True)

        mock_utils.update_device_state.side_effect = exceptions.InvalidDeviceError('mock test error')

        response = self.veralite.turn_off_switch(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_device_state.called, "update device method not present")
        self.assertEqual(response['result'], False)

    @patch('veralite.veralite.utils')
    def test_arm_motion_sensor(self, mock_utils):
        self.veralite.update_devices()
        data = json.loads(_RESPONSE_STRING)
        mock_utils.update_sensor_state.return_value = {'result': True, 'message': data}

        response = self.veralite.arm_motion_sensor(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_sensor_state.called, "update device method not present")
        self.assertEqual(response['result'], True)

        mock_utils.update_sensor_state.side_effect = exceptions.InvalidDeviceError('mock test error')

        response = self.veralite.arm_motion_sensor(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_sensor_state.called, "update device method not present")
        self.assertEqual(response['result'], False)

    @patch('veralite.veralite.utils')
    def test_disarm_motion_sensor(self, mock_utils):
        self.veralite.update_devices()
        data = json.loads(_RESPONSE_STRING)
        mock_utils.update_sensor_state.return_value = {'result': True, 'message': data}

        response = self.veralite.disarm_motion_sensor(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_sensor_state.called, "update device method not present")
        self.assertEqual(response['result'], True)

        mock_utils.update_sensor_state.side_effect = exceptions.InvalidDeviceError('mock test error')

        response = self.veralite.disarm_motion_sensor(self.veralite.switches[4])

        self.assertTrue(mock_utils.update_sensor_state.called, "update device method not present")
        self.assertEqual(response['result'], False)


if __name__ == '__main__':
    unittest.main()
