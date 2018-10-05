from .tiltify3 import Tiltify3, Tiltify3Result
from .avatar import VideoResult, ImageResult, AvatarResult, LogoResult, BannerResult


class FundraisingEventResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'slug',
        'url',
        'description',
        'bannerTitle',
        'bannerIntro',
        'currency',
        'goal',
        'amountRaised',
        'startsOn',
        'endsOn',
        'causeId',
    ]
    FIELDS_SUB = {
        'video': VideoResult,
        'image': ImageResult,
        'avatar': AvatarResult,
        'logo': LogoResult,
        'banner': BannerResult,
    }
