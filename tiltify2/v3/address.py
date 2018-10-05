from .tiltify3 import Tiltify3, Tiltify3Result


class AddressResult(Tiltify3Result):
    FIELDS_NORM = [
        'addressLine1',
        'addressLine2',
        'city',
        'region',
        'postalCode',
        'country',
    ]
    FIELDS_SUB = {}
