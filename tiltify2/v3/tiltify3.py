import json
import requests
from json import JSONDecodeError


class Tiltify3Result(object):
    FIELDS_NORM = []
    FIELDS_SUB = {}

    RESTRICTED_FIELDS = set([
        'id',
        'status',
        'data',
        'links',
        'url_self',
        'url_next',
        'url_prev',
    ])

    def __init__(self, meta_status, data, links):
        self.status = int(meta_status)
        self.data = data
        self.links = links

        self.parsed = self.parse()
        self.parsed.update(dict(status=self.status, data=self.data, links=self.links))

    def parse(self):
        ret = self.parse_data()
        ret.update(self.parse_links())
        # Set fields to whatever parse_data returns
        for k, v in ret.items():
            setattr(self, "data_%s" % k, v)
        return ret

    def parse_data(self):
        ret = {}
        for key in self.FIELDS_NORM:
            ret[key] = self.data.get(key, None)
        for key, t in self.FIELDS_SUB.items():
            if key in self.data:
                ret[key] = t(**self.data[key])
            else:
                ret[key] = None
        return ret

    def parse_links(self):
        """ Parse link info """
        ret = {}
        for k, v in self.links.items():
            if v:
                ret["url_%s" % k] = v
        return ret


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

    def getr(self, result_type, url, data, **kwargs):
        """ Run a GET request - return the given result type response """
        r = self.get(url=url, data=data, **kwargs)
        res = result_type(
            meta_status=r.get('meta', {}).get('status', None),
            data=r.get('data', None),
            links=r.get('links', {}),
        )

    def _default_args(self):
        return dict(api_key=self.api_key, timeout=self.timeout, extra_headers=self.extra_headers)

    @property
    def campaign(self):
        from .campaigns import CampaignTiltify
        return CampaignTiltify(**self._default_args())
