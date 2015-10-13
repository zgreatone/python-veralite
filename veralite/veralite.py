#!/usr/bin/python
"""Veralite™
   Okpe Pessu <opessu@zgreatone.net>
"""
import simplejson as json
import requests
import random
from requests.auth import HTTPDigestAuth

URL_ENDPOINT = '/port_3480/data_request?id=user_data'


class Veralite:
    def __init__(self, ip, user=None, password=None):
        self.ip = ip
        self.user = user
        self.password = password

    def get_data(self):
        """
        Method gets data through http request from veralite
        :return:
        """
        user = self.user
        password = self.password
        ip = self.ip
        p = {'rand': random.random()}
        url = "http://" + ip + URL_ENDPOINT
        if user is not None and password is not None:
            response = requests.get(url,
                                    params=p,
                                    auth=HTTPDigestAuth(user, password))
        else:
            response = requests.get(url,
                                    params=p)

        response_content = json.loads(response.__dict__['_content'])

        return response_content
