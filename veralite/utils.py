#!/usr/bin/python
"""Utilities for Python Veralite™ Module
   Okpe Pessu <opessu@zgreatone.net>

   Module to hold utility methods to help with connection and data formatting
"""
import simplejson as json
import random
import requests

from requests.auth import HTTPDigestAuth

LIGHT_ENDPOINT = "/port_3480/data_request?id=lu_action&output_format=json&action=SetTarget"
LIGHT_SERVICE = "urn:upnp-org:serviceId:SwitchPower1"

DIMMING_ENDPOINT = "/port_3480/data_request?id=lu_action&output_format=json&action=SetLoadLevelTarget"
DIMMING_SERVICE = "urn:upnp-org:serviceId:Dimming1"

SENSOR_ENDPOINT = "/port_3480/data_request?id=lu_action&output_format=json&action=SetArmed"
SENSOR_SERVICE = "urn:micasaverde-com:serviceId:SecuritySensor1"


def perform_request(vera_ip, user, password, url_endpoint, params):
    # TODO error checking
    params['rand'] = random.random()
    url = "http://" + vera_ip + url_endpoint

    # TODO handle exception in the case of connection issues
    if user is not None and password is not None:
        response = requests.get(url,
                                params=params,
                                auth=HTTPDigestAuth(user, password))
    else:
        response = requests.get(url,
                                params=params)

    response_content = json.loads(response.__dict__['_content'])

    return response_content


def update_brightness(vera_ip, user, password, device, target_brightness):
    # check to make sure device is of type DimmingLight

    params = {'serviceId': DIMMING_SERVICE, 'DeviceNum': device.identifier,
              'newLoadlevelTarget': target_brightness}

    response_content = perform_request(vera_ip, user, password, DIMMING_ENDPOINT, params)

    if "ERROR" not in response_content:
        return {'result': True}
    else:
        return {'result': False, 'message': response_content}


def update_sensor_state(vera_ip, user, password, device, new_state):
    # check to make sure device is of type Sensor

    params = {'serviceId': SENSOR_SERVICE, 'DeviceNum': device.identifier, 'newArmedValue': new_state}

    response_content = perform_request(vera_ip, user, password, SENSOR_ENDPOINT, params)

    if "ERROR" not in response_content:
        return {'result': True}
    else:
        return {'result': False, 'message': response_content}


def update_device_state(vera_ip, user, password, device, new_state):
    # check to make sure device is of type Light/DimmingLight/Switch

    params = {'serviceId': LIGHT_SERVICE, 'DeviceNum': device.identifier, 'newTargetValue': new_state}

    response_content = perform_request(vera_ip, user, password, LIGHT_ENDPOINT, params)

    if "ERROR" not in response_content:
        return {'result': True}
    else:
        return {'result': False, 'message': response_content}
