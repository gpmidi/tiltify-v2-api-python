from .tiltify3 import Tiltify3, Tiltify3Result
from .avatar import AvatarResult
from .social import SocialResult


class TeamResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'slug',
        'url',
    ]
    FIELDS_SUB = {
        'avatar': AvatarResult,
    }


class OwnedTeamResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'slug',
        'url',
        'bio',
        'inviteOnly',
        'disbanded',
    ]
    FIELDS_SUB = {
        'avatar': AvatarResult,
        'social': SocialResult,
    }


class UserTeamResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'slug',
        'url',
    ]
    FIELDS_SUB = {
        'avatar': AvatarResult,
    }
