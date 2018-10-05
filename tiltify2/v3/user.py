from .tiltify3 import Tiltify3, Tiltify3Result
from .avatar import AvatarResult


class UserResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'username',
        'slug',
        'url',
    ]
    FIELDS_SUB = {
        'avatar': AvatarResult,
    }

    def parse_data(self):
        ret = {}
        for key in self.FIELDS_NORM:
            ret[key] = self.data.get(key, None)
