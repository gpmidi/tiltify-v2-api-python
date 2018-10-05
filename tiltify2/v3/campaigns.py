from .tiltify3 import Tiltify3, Tiltify3Result
from .livestream import LiveStreamResult
from .avatar import AvatarResult
from .user import UserResult
from .team import TeamResult


class CampaignResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'slug',
        'url',
        'startsAt',
        'endsAt',
        'description',
        'causeId',
        'fundraisingEventId',
        'fundraiserGoalAmount',
        'originalGoalAmount',
        'amountRaised',
        'supportingAmountRaised',
        'totalAmountRaised',
        'supportable',
        'status',
    ]
    FIELDS_SUB = {
        'avatar': AvatarResult,
        'user': UserResult,
        'team': TeamResult,
        'livestream': LiveStreamResult,
    }
