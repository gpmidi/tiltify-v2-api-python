from .tiltify3 import Tiltify3, Tiltify3Result


class MediaResult(Tiltify3Result):
    FIELDS_NORM = [
        'src',
        'alt',
        'width',
        'height',
    ]
    FIELDS_SUB = {}


class ImageResult(MediaResult):
    pass


class VideoResult(MediaResult):
    pass


class AvatarResult(ImageResult):
    pass


class LogoResult(ImageResult):
    pass


class BannerResult(ImageResult):
    pass
