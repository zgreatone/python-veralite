#!/usr/bin/python
"""Utilities for Python Veralite™ Module
   Okpe Pessu <opessu@zgreatone.net>

   Module to hold utility methods to help with connection and data formatting
"""
import simplejson as json
import random
import requests
import logging

from requests.auth import HTTPDigestAuth
from requests.exceptions import Timeout
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError

from device import Light
from device import DimmingLight
from device import Switch
from device import MotionSensor

from exceptions import InvalidDeviceError
from exceptions import VeraliteConnectionError

# create logger
logger = logging.getLogger('utils')

_DEFUALT_TIMEOUT = 5

# ERROR_CODES
_CONNECTION_ISSUE = "0"
_HTTP_ERROR = "1"

LIGHT_ENDPOINT = "/port_3480/data_request?id=lu_action&output_format=json&action=SetTarget"
LIGHT_SERVICE = "urn:upnp-org:serviceId:SwitchPower1"

DIMMING_ENDPOINT = "/port_3480/data_request?id=lu_action&output_format=json&action=SetLoadLevelTarget"
DIMMING_SERVICE = "urn:upnp-org:serviceId:Dimming1"

SENSOR_ENDPOINT = "/port_3480/data_request?id=lu_action&output_format=json&action=SetArmed"
SENSOR_SERVICE = "urn:micasaverde-com:serviceId:SecuritySensor1"


def perform_get_request(vera_ip, user, password, url_endpoint, params, timeout=_DEFUALT_TIMEOUT):
    """

    :param vera_ip:
    :param user:
    :param password:
    :param url_endpoint:
    :param params:
    :param timeout:
    :return:
    """
    params['rand'] = random.random()
    url = "http://" + vera_ip + url_endpoint

    # put in a try block to handle request connection issues
    try:
        response = requests.get(url,
                                timeout=timeout,
                                params=params,
                                auth=HTTPDigestAuth(user, password))

        if response.status_code == requests.codes.ok:
            # response is ok so return content from dictionary
            response_content = json.loads(response.__dict__['_content'])

            return response_content

        else:
            response.raise_for_status()

    except (ConnectionError, Timeout) as e:
        logger.error("connection issues when performing request " + str(e))
        raise VeraliteConnectionError(_CONNECTION_ISSUE, "connection issues")
    except HTTPError as e:
        logger.error("http error when performing request " + str(e))
        raise VeraliteConnectionError(_HTTP_ERROR, "http error")


def update_brightness(vera_ip, user, password, device, target_brightness):
    # check to make sure device is of type DimmingLight
    if type(device) is not DimmingLight:
        raise InvalidDeviceError("device is of wrong type")

    params = {'serviceId': DIMMING_SERVICE, 'DeviceNum': device.identifier,
              'newLoadlevelTarget': target_brightness}

    response_content = perform_get_request(vera_ip, user, password, DIMMING_ENDPOINT, params)

    if "ERROR" not in response_content:
        return {'result': True, 'message': response_content}
    else:
        return {'result': False, 'message': response_content}


def update_sensor_state(vera_ip, user, password, device, new_state):
    # check to make sure device is of type Sensor
    if type(device) is not MotionSensor:
        raise InvalidDeviceError("device is of wrong type")

    params = {'serviceId': SENSOR_SERVICE, 'DeviceNum': device.identifier, 'newArmedValue': new_state}

    response_content = perform_get_request(vera_ip, user, password, SENSOR_ENDPOINT, params)

    if "ERROR" not in response_content:
        return {'result': True, 'message': response_content}
    else:
        return {'result': False, 'message': response_content}


def update_device_state(vera_ip, user, password, device, new_state):
    # check to make sure device is of type Light/DimmingLight/Switch
    if type(device) is not Light and type(device) is not DimmingLight and type(device) is not Switch:
        raise InvalidDeviceError("device is of wrong type")

    params = {'serviceId': LIGHT_SERVICE, 'DeviceNum': device.identifier, 'newTargetValue': new_state}

    response_content = perform_get_request(vera_ip, user, password, LIGHT_ENDPOINT, params)

    if "ERROR" not in response_content:
        return {'result': True, 'message': response_content}
    else:
        return {'result': False, 'message': response_content}
