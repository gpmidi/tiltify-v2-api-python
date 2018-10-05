from .tiltify3 import Tiltify3, Tiltify3Result


class ChallengeResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'amount',
        'totalAmountRaised',
        'active',
        'activatesOn',
        'campaignId',
        'endsAt',
        'createdAt',
        'updatedAt',
    ]
    FIELDS_SUB = {}
