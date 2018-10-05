from .tiltify3 import Tiltify3, Tiltify3Result


class SocialResult(Tiltify3Result):
    FIELDS_NORM = [
        'twitter',
        'youtube',
        'facebook',
        'instagram',
        'website',
    ]
    FIELDS_SUB = {}
