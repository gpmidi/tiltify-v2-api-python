from .tiltify3 import Tiltify3, Tiltify3Result
from .avatar import ImageResult


class PollOptionsResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'pollId',
        'name',
        'totalAmountRaised',
        'createdAt',
        'updatedAt',
    ]
    FIELDS_SUB = {}


class PollResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'active',
        'campaignId',
        'createdAt',
        'updatedAt',
    ]
    FIELDS_SUB = {
        'options': PollOptionsResult,
    }
