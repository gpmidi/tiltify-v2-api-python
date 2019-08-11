import json
import requests
from json import JSONDecodeError


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
    BASE_URL = 'https://tiltify.com/api/v3'

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

    # Fetchers of data

    ## Campaign Based
    def f_campaign(self, pk):
        from .campaigns import CampaignResult
        # https://tiltify.github.io/api/entities/campaign.html
        return self.getr(CampaignResult, self.BASE_URL + "/campaigns/%s" % pk)

    def f_campaigns(self):
        from .campaigns import CampaignResult
        # https://tiltify.github.io/api/entities/campaign.html
        return self.getrl(CampaignResult, self.BASE_URL + "/campaigns")

    def f_campaign_donations(self, pk):
        from .donation import DonationResult
        #
        return self.getrl(DonationResult, self.BASE_URL + "/campaigns/%s/donations" % pk)

    def f_campaign_rewards(self, pk):
        from .reward import RewardResult
        #
        return self.getrl(RewardResult, self.BASE_URL + "/campaigns/%s/rewards" % pk)

    def f_campaign_polls(self, pk):
        from .poll import PollResult
        #
        return self.getrl(PollResult, self.BASE_URL + "/campaigns/%s/polls" % pk)

    def f_campaign_challenges(self, pk):
        from .challenges import ChallengeResult
        #
        return self.getrl(ChallengeResult, self.BASE_URL + "/campaigns/%s/challenges" % pk)

    def f_campaign_schedule(self, pk):
        from .schedule import ScheduleResult
        #
        return self.getrl(ScheduleResult, self.BASE_URL + "/campaigns/%s/schedule" % pk)

    def f_campaign_supporting_campaigns(self, pk):
        from .campaigns import SupportingCampaignResult
        #
        return self.getrl(SupportingCampaignResult, self.BASE_URL + "/campaigns/%s/supporting-campaigns" % pk)

    ## Team based
    def f_team(self, pk):
        from .team import TeamResult
        # https://tiltify.github.io/api/entities/team.html
        return self.getr(TeamResult, self.BASE_URL + "/teams/%s" % pk)

    def f_teams(self):
        from .team import TeamResult
        # https://tiltify.github.io/api/entities/team.html
        return self.getrl(TeamResult, self.BASE_URL + "/teams")

    def f_team_campaigns(self, pk):
        from .campaigns import TeamCampaignResult
        # https://tiltify.github.io/api/endpoints/teams-id-campaigns.html
        return self.getrl(TeamCampaignResult, self.BASE_URL + "/teams/%s/campaigns" % pk)

    def f_team_campaign(self, teamId, campaignId):
        from .campaigns import CampaignResult
        # https://tiltify.github.io/api/endpoints/teams-id-campaigns-id.html
        return self.getr(CampaignResult, self.BASE_URL + "/teams/%s/campaigns/%s" % (teamId, campaignId))

    ## User Based
    def f_self(self):
        from .user import UserResult
        # https://tiltify.github.io/api/endpoints/user.html
        return self.getr(UserResult, self.BASE_URL + "/user")

    def f_user(self, pk):
        from .user import UserResult
        # https://tiltify.github.io/api/entities/user.html
        return self.getr(UserResult, self.BASE_URL + "/users/%s" % pk)

    def f_users(self):
        from .user import UserResult
        # https://tiltify.github.io/api/entities/user.html
        return self.getrl(UserResult, self.BASE_URL + "/users")

    def f_user_campaigns(self, userId):
        from .campaigns import UserCampaignResult
        # https://tiltify.github.io/api/endpoints/users-id-campaigns.html
        return self.getrl(UserCampaignResult, self.BASE_URL + "/users/%s/campaigns" % userId)

    def f_user_campaign(self, userId, campaignId):
        from .campaigns import CampaignResult
        # https://tiltify.github.io/api/endpoints/users-id-campaigns-id.html
        return self.getr(CampaignResult, self.BASE_URL + "/users/%s/campaigns/%s" % (userId, campaignId))

    def f_user_owned_teams(self, userId):
        from .team import OwnedTeamResult
        # https://tiltify.github.io/api/endpoints/users-id-owned-teams.html
        return self.getrl(OwnedTeamResult, self.BASE_URL + "/users/%s/teams" % userId)

    def f_user_teams(self, userId):
        from .team import UserTeamResult
        # https://tiltify.github.io/api/endpoints/users-id-teams.html
        return self.getrl(UserTeamResult, self.BASE_URL + "/users/%s/campaigns" % userId)

    ## Cause Based
    def f_cause(self, pk):
        from .cause import CauseResult
        # https://tiltify.github.io/api/entities/cause.html
        return self.getr(CauseResult, self.BASE_URL + "/causes/%s" % pk)

    def f_causes(self):
        from .cause import CauseResult
        # https://tiltify.github.io/api/entities/cause.html
        return self.getrl(CauseResult, self.BASE_URL + "/causes")

    # TODO: Support more types for causes

    ## Fund Based
    def f_fund_event(self, pk):
        from .fundraising_event import FundraisingEventResult
        # https://tiltify.github.io/api/entities/fundraising-event.html
        return self.getr(FundraisingEventResult, self.BASE_URL + "/fundraising-events/%s" % pk)

    def f_fund_events(self):
        from .fundraising_event import FundraisingEventResult
        # https://tiltify.github.io/api/entities/fundraising-event.html
        return self.getrl(FundraisingEventResult, self.BASE_URL + "/fundraising-events")

    # TODO: Support more types for fundraising events
