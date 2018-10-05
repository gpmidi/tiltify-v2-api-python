from .tiltify3 import Tiltify3, Tiltify3Result


class ScheduleResult(Tiltify3Result):
    FIELDS_NORM = [
        'id',
        'name',
        'description',
        'startsAt',
    ]
    FIELDS_SUB = {}
