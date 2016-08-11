##############################################################################
#
# @author:  Noè Murr
# @file:    Longitude.py
# @brief:   contains the definition of Longitude class.
#
##############################################################################

__author__ = "Noè Murr"


class Longitude:
    """ Simple class representing the concept of Navigational longitude """

    def __init__(self, degrees: float = 0.0, minutes: float = 0.0, seconds: float = 0.0, sign: str = 'E'):
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
        """ Assign operator for checking variable """

        if "sign" == key:
            # checking sign
            try:
                value = str(value)
            except ValueError as e:
                e.message = "Sign must be a string E (East) or W (West)"
                raise
            else:
                if value != 'E' and value != 'W':
                    raise ValueError("Sign must be a string E (East) or W (West)")
                else:
                    super().__setattr__(key, value)

        # checking degrees value
        elif "degrees" == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                e.message = "degrees must be a numerical value"
                raise
            else:
                if value > 180:
                    raise ValueError("Longitude cannot be greater than 180 degrees")
                elif 180 == value and (self.minutes > 0 or self.seconds > 0):
                    raise ValueError("Longitude cannot be greater than 180 degrees")
                else:
                    deg = float(int(value))
                    minutes = self.minutes + ((value - int(value)) * 60)

                    sec = self.seconds + ((minutes - int(minutes)) * 60)
                    minutes = float(int(minutes))

                    minutes += sec // 60
                    sec %= 60

                    deg += minutes // 60
                    minutes %= 60

                    if deg > 180 or (deg == 180 and (minutes > 0 or sec > 0)):
                        raise ValueError("Longitude cannot be greater than 180 degrees")
                    else:
                        super().__setattr__('degrees', deg)
                        super().__setattr__('minutes', minutes)
                        super().__setattr__('seconds', sec)

        # checking minutes value
        elif "minutes" == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                e.message = "minutes must be a numerical value"
                raise
            else:
                mins = float(int(value))
                secs = self.seconds + ((mins - int(mins)) * 60)

                if secs > 60:
                    mins += secs // 60
                    secs %= 60

                if mins >= 60:
                    degs = self.degrees + (mins // 60)
                    mins %= 60

                    if degs > 180 or (180 == degs and (mins > 0 or secs > 0)):
                        raise ValueError("Longitude cannot be greater than 180 degrees")
                    else:
                        super().__setattr__('degrees', degs)

                super().__setattr__('minutes', mins)
                super().__setattr__('seconds', secs)

        # checking minutes value
        elif "seconds" == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                e.message = "seconds must be a numerical value"
                raise
            else:
                if value > 60:
                    mins = self.minutes + (value // 60)
                    value %= 60

                    if mins > 60:
                        degs = self.degrees + (mins // 60)
                        mins %= 60

                        if degs > 180 or (180 == degs and (mins > 0 or value > 0)):
                            raise ValueError("Longitude cannot be greater than 180 degrees")
                        else:
                            super().__setattr__('degrees', degs)
                            super().__setattr__('minutes', mins)
                            super().__setattr__('seconds', value)

                    else:
                        super().__setattr__('minutes', mins)
                        super().__setattr__('seconds', value)
                else:
                    super().__setattr__('seconds', value)

        # if I don't care about the value I'll set it
        else:
            super().__setattr__(key, value)

    def __str__(self):
        return "{}° {}' {}\" {}".format(int(self.degrees), int(self.minutes), int(self.seconds), self.sign)

    def __float__(self):
        value = self.degrees + (self.minutes/60) + (self.seconds / 3600)
        value = value if self.sign == 'E' else value * -1
        return value

    def __add__(self, other):
        """
        Method that permits to sum a longitude with a LongitudeDistance or a tuple like this: (deg, mins, secs, sign).
        Cannot sum Longitude with Longitude because this operation has no graphical sense so to do an operation like
        that you should cast the Longitudes type values in float values.
        :param other: LongitudeDistance obj or tuple that will be interpreted like a LongitudeDistance obj
        :return: Longitude type
        """
        if type(other) == type(self):
            raise TypeError("Cannot sum Longitude with Longitude because"
                            " this operation has no graphical sense so to do an operation like"
                            " that you should cast the Longitudes type values in float values.")

        # sum with tuple of type (degs, mins, secs, sign)
        elif type(other) == tuple and 4 == len(other):
            try:
                other[0] = abs(float(other[0]))
                other[1] = abs(float(other[1]))
                other[2] = abs(float(other[2]))
                other[3] = str(other[3])
            except ValueError as e:
                e.message = 'the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)'
                raise
            else:
                other = LongitudeDistance(other)
                return self.__add__(other)
        elif type(other) == LongitudeDistance:
            result = float(self) + float(other)
            return floattolongitude(result)

        else:
            if type(other) == tuple:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                raise TypeError("Cannot add Longitude with {}".format(type(other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """
        Method that permits to subtract 'something' to a Longitude object, if other is another Longitude object
        the method return an LongitudeDistance object containing the distance between other and self Longitudes
        else if other is of type LongitudeDistance the method returns a Longitude value representing the meridian
        that is at LongitudeDistance from self Longitude, else if other is a tuple like (degs, mins, secs, sign)
        it is interpreted like a Longitude object so it's returned a LongitudeDistance object.
        :param other: LongitudeDistance value or tuple like: (deg, mins, secs, sign).
        :return: the LongitudeDistance between other and self longitudes
        """
        # sub of two longitudes
        if type(other) == type(self):
            # the distance between other and self is returned because:
            # if the user write lonDist = longB - longA he wants the distance between
            # longA and longB (Mathematically it is what is obtained by this operation)
            return LongitudeDistance(other, self)

        elif type(other) == tuple and 4 == len(other):
            try:
                other[0] = abs(float(other[0]))
                other[1] = abs(float(other[1]))
                other[2] = abs(float(other[2]))
                other[3] = str(other[3])
            except ValueError as e:
                e.message = 'the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)'
                raise
            return LongitudeDistance(Longitude(*other), self)

        elif type(other) == LongitudeDistance:
            result = float(self) - float(other)
            return floattolongitude(result)

        else:
            if type(other) == tuple:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                raise TypeError("Cannot subtract Longitude with {}".format(type(other)))

    def __rsub__(self, other):
        if type(other) == type(self):
            return other.__sub__(self)

        elif type(other) == tuple and 4 == len(other):
            try:
                other[0] = abs(float(other[0]))
                other[1] = abs(float(other[1]))
                other[2] = abs(float(other[2]))
                other[3] = str(other[3])
            except ValueError as e:
                e.message = 'the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)'
                raise
            return Longitude(*other).__sub__(self)

        else:
            if type(other) == tuple:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                raise TypeError("Cannot subtract Longitude with {}".format(type(other)))


class LongitudeDistance:
    """
    Class that represents the concept of longitude distance between two Longitudes.
    To understand better the concept: the class answer at the Question:
    how many Degrees, minutes and seconds I must go to get from a to b?
    """
    def __init__(self, a, b=None):
        if type(a) == Longitude and type(b) == Longitude:
            pass
        elif type(a) == Longitude and type(b) == tuple:
            pass
        elif type(a) == tuple and type(b) == Longitude:
            pass
        elif type(a) == tuple and type(b) == tuple:
            pass
        elif type(a) == tuple and (b is None):
            pass
        else:
            raise TypeError("Cannot make a LongitudeDistance between {} and {}".format(type(a), type(b)))


def floattolongitude(x: float = 0.0) -> Longitude:
    try:
        x = float(x)
    except ValueError as e:
        e.message = "Cannot make a Longitude without a numerical value"
        raise
    else:
        if x < 0:
            sign = 'W'
        else:
            sign = 'E'

        return Longitude(degrees=abs(x), sign=sign)
