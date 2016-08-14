##############################################################################
#
# @author:  Noè Murr
# @file:    latitude.py
# @brief:   contains definition of Latitude.
#
##############################################################################

import math


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
            try:
                value = str(value)
            except ValueError as e:
                raise ValueError("Sign must be a string N (North) or S (South)") from e
            else:
                if "E" == value:
                    super().__setattr__(key, value)
                elif "W" == value:
                    super().__setattr__(key, value)
                else:
                    raise ValueError("Sign must be a string N (North) or S (South)")

        elif 'degrees' == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                raise ValueError("degrees must be a numerical value") from e
            else:
                if value > 90:
                    raise ValueError("Latitude cannot be greater than 90 degrees")
                elif 90 == value and (self.minutes > 0 or self.seconds > 0):
                    raise ValueError("Latitude cannot be greater than 90 degrees")
                else:
                    deg, frac = math.modf(value)
                    minutes, frac = math.modf(self.minutes + (frac * 60))

                    sec = self.seconds + (frac * 60)

                    minutes += sec // 60
                    sec %= 60

                    deg += minutes // 60
                    minutes %= 60

                    if deg > 90 or (90 == deg and (minutes > 0 or sec > 0)):
                        raise ValueError("Latitude cannot be greater than 180 degrees")
                    else:
                        super().__setattr__('degrees', deg)
                        super().__setattr__('minutes', minutes)
                        super().__setattr__('seconds', sec)

        elif 'minutes' == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                raise ValueError("minutes must be a numerical value") from e
            else:
                degs = self.degrees
                mins, frac = math.modf(value)
                secs = self.seconds + (frac * 60)

                if secs >= 60:
                    mins += secs // 60
                    secs %= 60

                if mins >= 60:
                    degs = self.degrees + (mins // 60)
                    mins %= 60

                if degs > 90 or (90 == degs and (mins > 0 or secs > 0)):
                    raise ValueError("Latitude cannot be greater than 90 degrees")
                else:
                    super().__setattr__('degrees', degs)
                    super().__setattr__('minutes', mins)
                    super().__setattr__('seconds', secs)

        elif 'seconds' == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                raise ValueError("seconds must be a numerical value") from e
            else:
                degs = self.degrees
                mins = self.minutes
                if value >= 60:
                    mins = self.minutes + (value // 60)
                    value %= 60

                    if mins >= 60:
                        degs = self.degrees + (mins // 60)
                        mins %= 60

                if degs > 90 or (90 == degs and (mins > 0 or value > 0)):
                    raise ValueError("Latitude cannot be greater than 90 degrees")
                else:
                    super().__setattr__('degrees', degs)
                    super().__setattr__('minutes', mins)
                    super().__setattr__('seconds', value)

        else:
            super().__setattr__(key, value)

    def __str__(self):
        if 0 == self.degrees and 0 == self.minutes and 0 == self.seconds:
            return '{}° {}\' {}" {}'.format(self.degrees, self.minutes, self.seconds, 'N/S')
        else:
            return '{}° {}\' {}" {}'.format(self.degrees, self.minutes, self.seconds, self.sign)

    def __float__(self):
        value = self.degrees + (self.minutes / 60) + (self.seconds / 3600)
        value = value if self.sign == 'E' else value * -1
        return value

    def __add__(self, other):
        """
        Method that permits to sum a Latitude with a LatitudeDistance or a tuple like this: (deg, mins, secs, sign).
        Cannot sum Latitude with Latitude because this operation has no graphical sense so to do an operation like
        that you should cast the Latitude type values in float values.
        :param other: LatitudeDistance obj or tuple that will be interpreted like a LongitudeDistance obj
        :return: Latitude type
        """
        if type(other) == type(self):
            raise TypeError('cannot sum two Latitude objects: it has no graphic sense, to do that cast Longitudes into'
                            'floats value')

        elif type(other) == tuple:
            try:
                a = abs(float(other[0]))
                b = abs(float(other[1]))
                c = abs(float(other[2]))
                d = str(other[3])
            except ValueError as e:
                raise ValueError('the tuple must be like: '
                                 '(degrees: float, minutes: float, seconds: float, sign: str)') from e
            else:
                other = LatitudeDistance((a, b, c, d))
                return self.__add__(other)

        elif type(other) == LatitudeDistance:
            return floattolatitude(float(self) + float(other))

        else:
            raise TypeError('cannot sum Longitude with {}'.format(type(other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """
        Method that permits to subtract 'something' to a Latitude object, if other is another Latitude object
        the method returns a LatitudeDistance object containing the distance between other and self Latitudes
        else if other is of type LatitudeDistance the method returns a Latitude value representing the parallel
        that is at LatitudeDistance from self Latitude, else if other is a tuple like (degs, mins, secs, sign)
        it is interpreted like a Latitude object so it's returned a LatitudeDistance object.
        :param other: LatitudeDistance value or tuple like: (deg, mins, secs, sign).
        :return: the LatitudeDistance between other and self longitudes
        """
        if type(other) == type(self):
            # the distance between other and self is returned because:
            # if the user write lonDist = longB - longA he wants the distance between
            # longA and longB (Mathematically it is what is obtained by this operation)
            return LatitudeDistance(other, self)

        elif type(other) == tuple:
            if len(other) == 4:
                try:
                    a = float(other[0])
                    b = float(other[1])
                    c = float(other[2])
                    d = str(other[3])
                except ValueError as e:
                    raise ValueError('tuple must be of type (degrees, minutes, seconds, sign)') from e
                else:
                    return LatitudeDistance(Latitude(a, b, c, d), self)
            else:
                raise ValueError('tuple must be like (degrees, minutes, seconds,sign)')

        elif type(other) == LatitudeDistance:
            a = float(self)
            b = float(other)
            return floattolatitude(a-b)

        else:
            raise TypeError("cannot sub {} with {}".format(type(self), type(other)))

    def __rsub__(self, other):
        if type(other) == tuple and len(other) != 4:
            b = self
            a = LatitudeDistance(other)
            return a - b

        else:
            raise TypeError("cannot rsub {} with {}".format(type(self), type(other)))


class LatitudeDistance:
    def __init__(self,  a=(0, 0, 0, 'E'), b=None):
        pass

    def __setattr__(self, key, value):
        pass

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


def floattolatitude(value: float = 0.0) -> Latitude:
    try:
        value = float(value)
    except ValueError as e:
        raise ValueError('value must be a numerical value') from e
    else:
        sign = 'N' if value >= 0 else 'S'

        return Latitude(degrees=abs(value), sign=sign)


def floattolatitudedistance(value: float = 0.0) -> LatitudeDistance:
    try:
        value = float(value)
    except ValueError as e:
        raise ValueError('value must be a numerical value') from e
    else:
        sign = 'N' if value >= 0 else 'S'

        return LatitudeDistance((value, 0, 0, sign))
