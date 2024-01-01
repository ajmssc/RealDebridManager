from abc import abstractmethod
from typing import Protocol

import requests


class WithRDAPIInterface(Protocol):

    def _get(self, path, json=True):
        raise NotImplementedError

    def _put(self, path, json=True, data=None):
        raise NotImplementedError

    def _post(self, path, json=True, data=None):
        raise NotImplementedError

    def _delete(self, path, json=True):
        raise NotImplementedError


class WithRDAPI:

    def __init__(self, api_token):
        self.api_token = api_token
        self.api_url = "https://api.real-debrid.com/rest/1.0"
        self.headers = {'Authorization': 'Bearer ' + self.api_token}

    def _get(self, path, json=True):
        response = requests.get(self.api_url + path, headers=self.headers)
        if json:
            return response.json()
        else:
            return response.text

    def _put(self, path, json=True, data=None):
        response = requests.put(self.api_url + path, headers=self.headers, data=data)
        if json:
            return response.json()
        else:
            return response.text

    def _post(self, path, json=True, data=None):
        response = requests.post(self.api_url + path, headers=self.headers, data=data)
        if json:
            return response.json()
        else:
            return response.text

    def _delete(self, path, json=True):
        response = requests.delete(self.api_url + path, headers=self.headers)
        if json:
            return response.json()
        else:
            return response.text
