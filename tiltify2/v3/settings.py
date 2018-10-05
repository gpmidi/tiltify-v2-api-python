from .tiltify3 import Tiltify3, Tiltify3Result


class ColorsResult(Tiltify3Result):
    FIELDS_NORM = [
        'background',
        'highlight',
    ]
    FIELDS_SUB = {}


class SettingsResult(Tiltify3Result):
    FIELDS_NORM = [
        'headerIntro',
        'headerTitle',
        'footerCopyright',
        'findOutMoreLink',
    ]
    FIELDS_SUB = {
        'colors': ColorsResult,
    }

