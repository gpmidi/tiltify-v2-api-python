import json
import requests
from json import JSONDecodeError


class Tiltify3(object):
    def __init__(self, api_key, timeout=2, extra_headers=None):
        self.api_key = api_key
        self._session = None
        self.timeout = timeout
        self.extra_headers = extra_headers

    def session(self, **kwargs):
        if not self._session:
            self._session = requests.Session()
            # Add auth header
            self._session.headers.update(self.auth_header())
            # Add any extra headers, if defined
            if self.extra_headers:
                self._session.headers.update(self.extra_headers)

        return self._session

    def auth_header(self):
        return {'Authorization': 'Bearer {}'.format(self.api_key)}

    def get(self, url, data, **kwargs):
        """ Run a GET request """
        resp = self.session().get(
            url,
            data=data,
            timeout=self.timeout,
            **kwargs
        )
        resp.raise_for_status()

        try:
            return resp.json()
        except JSONDecodeError as e:
            return resp.text
