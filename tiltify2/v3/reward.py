from .tiltify3 import Tiltify3, Tiltify3Result
from .avatar import ImageResult


class RewardResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'description',
        'amount',
        'kind',
        'quantity',
        'remaining',
        'fairMarketValue',
        'currency',
        'shippingAddressRequired',
        'shippingNote',
        'active',
        'startsAt',
        'createdAt',
        'updatedAt',
    ]
    FIELDS_SUB = {
        'image': ImageResult,
    }
