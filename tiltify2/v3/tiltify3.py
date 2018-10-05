import json
import requests
from json import JSONDecodeError

# Various result types
from .campaigns import CampaignResult
from .livestream import LiveStreamResult
from .avatar import AvatarResult
from .user import UserResult
from .team import TeamResult
from .cause import CauseResult
from .fundraising_event import FundraisingEventResult

class Tiltify3Result(object):
    FIELDS_NORM = []
    FIELDS_SUB = {}

    RESTRICTED_FIELDS = {'id', 'status', 'data', 'links', 'url_self', 'url_next', 'url_prev'}

    def __init__(self, meta_status, data, links, error, errors):
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
    # Base API URL
    BASE_URL = 'https://tiltify.com/api/v3/'

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

    def get(self, url, data=None, **kwargs):
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

    def getr(self, result_type, url, data=None, **kwargs):
        """ Run a GET request - return the given result type response """
        r = self.get(url=url, data=data, **kwargs)
        res = result_type(
            meta_status=r.get('meta', {}).get('status', None),
            data=r.get('data', {}),
            links=r.get('links', {}),
            error=r.get('error', {}),
            errors=r.get('errors', {}),
        )

    def getrl(self, result_type, url, data=None, **kwargs):
        """ Run a GET request - yield the given result type response list """
        for r in self.get(url=url, data=data, **kwargs):
            yield result_type(
                meta_status=r.get('meta', {}).get('status', None),
                data=r.get('data', {}),
                links=r.get('links', {}),
                error=r.get('error', {}),
                errors=r.get('errors', {}),
            )

    def _default_args(self):
        return dict(api_key=self.api_key, timeout=self.timeout, extra_headers=self.extra_headers)

    def f_campaign(self, pk):
        # https://tiltify.github.io/api/entities/campaign.html
        return self.getr(CampaignResult, self.BASE_URL + "/campaigns/%d" % pk)

    def f_campaigns(self):
        # https://tiltify.github.io/api/entities/campaign.html
        return self.getrl(CampaignResult, self.BASE_URL + "/campaigns")

    def f_team(self, pk):
        # https://tiltify.github.io/api/entities/team.html
        return self.getr(TeamResult, self.BASE_URL + "/teams/%d" % pk)

    def f_teams(self):
        # https://tiltify.github.io/api/entities/team.html
        return self.getrl(TeamResult, self.BASE_URL + "/teams")

    def f_self(self):
        # https://tiltify.github.io/api/endpoints/user.html
        return self.getr(UserResult, self.BASE_URL + "/user")

    def f_user(self, pk):
        # https://tiltify.github.io/api/entities/user.html
        return self.getr(UserResult, self.BASE_URL + "/users/%d" % pk)

    def f_users(self):
        # https://tiltify.github.io/api/entities/user.html
        return self.getrl(UserResult, self.BASE_URL + "/users")

    def f_cause(self, pk):
        # https://tiltify.github.io/api/entities/cause.html
        return self.getr(CauseResult, self.BASE_URL + "/causes/%d" % pk)

    def f_causes(self):
        # https://tiltify.github.io/api/entities/cause.html
        return self.getrl(CauseResult, self.BASE_URL + "/causes")

    def f_fund_event(self, pk):
        # https://tiltify.github.io/api/entities/fundraising-event.html
        return self.getr(FundraisingEventResult, self.BASE_URL + "/fundraising-events/%d" % pk)

    def f_fund_events(self):
        # https://tiltify.github.io/api/entities/fundraising-event.html
        return self.getrl(FundraisingEventResult, self.BASE_URL + "/fundraising-events")
