from .tiltify3 import Tiltify3, Tiltify3Result


class LiveStreamResult(Tiltify3Result):
    FIELDS_NORM = [
        'channel',
        'type',
    ]
    FIELDS_SUB = {}
