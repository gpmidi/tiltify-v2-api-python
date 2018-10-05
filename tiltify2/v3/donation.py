from .tiltify3 import Tiltify3, Tiltify3Result


class DonationResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'amount',
        'name',
        'comment',
        'completedAt',
        'rewardId',
    ]
    FIELDS_SUB = {}
