##############################################################################
#
# @author:  Noè Murr
# @file:    latitude.py
# @brief:   contains definition of Latitude.
#
##############################################################################


class Latitude:

    def __init__(self, degrees: float = 0.0, minutes: float = 0.0, seconds: float = 0.0, sign: str = 'N'):
        """ Constructor for the class
        :type degrees:  float
        :type minutes:  float
        :type seconds:  float
        :type sign:     str
        """

        self.__dict__['degrees'] = 0.0
        self.__dict__['minutes'] = 0.0
        self.__dict__['seconds'] = 0.0
        self.sign = sign

        self.degrees = degrees
        self.minutes = minutes
        self.seconds = seconds

    def __setattr__(self, key, value):
        if 'sign' == key:
            pass
        elif 'degrees' == key:
            pass
        elif 'minutes' == key:
            pass
        elif 'seconds' == key:
            pass
        else:
            super().__setattr__(key, value)

    def __str__(self):
        pass  # TODO define the __str__ method

    def __float__(self):
        pass  # TODO define the __float__ method

    def __add__(self, other):
        pass  # TODO define the __add__ method

    def __radd__(self, other):
        pass  # TODO define the __radd__ method

    def __sub__(self, other):
        pass  # TODO define the __sub__ method

    def __rsub__(self, other):
        pass  # TODO define the __rsub__ method


class LatitudeDistance:
    pass


def floattolatitude(value: float = 0.0) -> Latitude:
    try:
        value = float(value)
    except ValueError as e:
        raise ValueError('value must be a numerical value') from e
    else:
        sign = 'N' if value >= 0 else 'S'

        return Latitude(degrees=abs(value), sign=sign)
