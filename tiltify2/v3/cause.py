from .tiltify3 import Tiltify3, Tiltify3Result
from .avatar import AvatarResult, LogoResult, BannerResult
from .address import AddressResult
from .social import SocialResult
from .settings import SettingsResult


class CauseResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'legalName',
        'slug',
        'currency',
        'about',
        'video',
        'contactEmail',
        'paypalEmail',
        'paypalCurrencyCode',
        'status',
        'stripeConnected',
        'mailchimpConnected',
    ]
    FIELDS_SUB = {
        'image': AvatarResult,
        'logo': LogoResult,
        'banner': BannerResult,
        'social': SocialResult,
        'settings': SettingsResult,
        'address': AddressResult,
    }
