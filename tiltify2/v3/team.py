from .tiltify3 import Tiltify3, Tiltify3Result
from .avatar import AvatarResult


class TeamResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'username',
        'slug',
        'url',
    ]
    FIELDS_SUB = {
        'avatar': AvatarResult,
    }
