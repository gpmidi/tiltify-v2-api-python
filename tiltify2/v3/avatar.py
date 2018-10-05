from .tiltify3 import Tiltify3, Tiltify3Result


class AvatarResult(Tiltify3Result):
    FIELDS_NORM = [
        'src',
        'alt',
        'width',
        'height',
    ]
    FIELDS_SUB = {}

    def parse_data(self):
        ret = {}
        for key in self.FIELDS_NORM:
            ret[key] = self.data.get(key, None)
