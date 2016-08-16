import math


class Latitude:
    """
    class that represents the Latitude Concept i.e. the distance in Degrees between Equator and a parallel.
    """
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

        # to avoid warnings I define the attributes with self
        self.degrees = 0.0
        self.minutes = 0.0
        self.seconds = 0.0

        self.sign = sign

        self.degrees += degrees
        self.minutes += minutes
        self.seconds += seconds

    def __setattr__(self, key, value):
        if 'sign' == key:
            try:
                value = str(value)
            except ValueError as e:
                raise ValueError("Sign must be a string N (North) or S (South)") from e
            else:
                if "N" == value:
                    super().__setattr__(key, value)
                elif "S" == value:
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
                    frac, deg = math.modf(value)
                    frac, minutes = math.modf(self.minutes + (frac * 60))

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
                frac, mins = math.modf(value)
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
            return '{}° {}\' {}" {}'.format(int(self.degrees), int(self.minutes), round(self.seconds, 2), 'N/S')
        else:
            return '{}° {}\' {}" {}'.format(int(self.degrees), int(self.minutes), round(self.seconds, 2), self.sign)

    def __float__(self):
        value = self.degrees + (self.minutes / 60) + (self.seconds / 3600)
        value = value if self.sign == 'N' else value * -1
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
            return float_to_latitude(float(self) + float(other))

        else:
            raise TypeError('cannot sum Latitude with {}'.format(type(other)))

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
            return float_to_latitude(a - b)

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
    """
    class to represent the distance between two different parallels. It can be from 0 degrees to 180 degrees North or
    South.
    """
    def __init__(self, a=(0, 0, 0, 'E'), b=None):
        self.__dict__['degrees'] = 0.0
        self.__dict__['minutes'] = 0.0
        self.__dict__['seconds'] = 0.0
        self.__dict__['sign'] = 'N'

        self.degrees = 0.0
        self.minutes = 0.0
        self.seconds = 0.0
        self.sign = 'N'

        if type(a) == Latitude and type(b) == Latitude:
            value = float(b) - float(a)
            self.sign = 'N' if value > 0 else 'S'
            self.degrees = abs(value)

        elif type(a) == Latitude and type(b) == tuple:
            try:
                deg, mins, sec, sign = abs(float(b[0])), abs(float(b[1])), abs(float(b[2])), str(b[3])
            except (ValueError, IndexError) as e:
                raise ValueError('Tuple must be like (degrees, minutes, seconds, sign)') from e
            else:
                if sign != 'N' and sign != 'S':
                    raise ValueError('Sign must be N North or S South')
                b = deg + mins / 60 + sec / 3600 if 'N' == sign else (deg + mins / 60 + sec / 3600) * -1
                value = b - float(a)
                self.sign = 'N' if value > 0 else 'S'
                self.degrees = abs(value)

        elif type(a) == tuple and type(b) == tuple:
            try:
                a_deg, a_min, a_sec, a_sign = abs(float(a[0])), abs(float(a[1])), abs(float(a[2])), str(a[3])
                b_deg, b_min, b_sec, b_sign = abs(float(b[0])), abs(float(b[1])), abs(float(b[2])), str(b[3])
            except (ValueError, IndexError)as e:
                raise ValueError('Tuple must be like (degrees, minutes, seconds, sign)') from e
            else:
                if (a_sign != 'N' and a_sign != 'S') or (b_sign != 'N' and b_sign != 'S'):
                    raise ValueError('Sign must be N North or S South')

                a = a_deg + a_min / 60 + a_sec / 3600 if 'N' == a_sign else (a_deg + a_min / 60 + a_sec / 3600) * -1
                b = b_deg + b_min / 60 + b_sec / 3600 if 'N' == b_sign else (b_deg + b_min / 60 + b_sec / 3600) * -1

                self.sign = 'N' if (b - a) > 0 else 'S'
                self.degrees = abs(b - a)

        elif type(a) == tuple and (b is None):
            try:
                deg, mins, sec, sign = abs(float(a[0])), abs(float(a[1])), abs(float(a[2])), str(a[3])
            except (ValueError, IndexError) as e:
                raise ValueError('Tuple must be like (degrees, minutes, seconds, sign)') from e
            else:
                if sign != 'N' and sign != 'S':
                    raise ValueError('Sign must be N North or S South')
                self.degrees += deg
                self.minutes += mins
                self.seconds += sec
                self.sign = sign

        else:
            raise TypeError("Cannot make a LatitudeDistance between {} and {}".format(type(a), type(b)))

    def __setattr__(self, key, value):
        if 'sign' == key:
            try:
                value = str(value)
            except ValueError as e:
                raise ValueError("Sign must be a string N North or S South") from e
            else:
                if value != 'N' and value != 'S':
                    raise ValueError("Sign must be a string N North or S South")
                else:
                    super().__setattr__(key, value)

        elif 'degrees' == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                raise ValueError("degrees must be a numerical value") from e
            else:
                if value > 180:
                    raise ValueError('Latitude distance cannot be greater than 180 degrees')
                elif 180 == value and (self.minutes > 0 or self.seconds > 0):
                    raise ValueError('Latitude distance cannot be greater than 180 degrees')
                else:
                    frac, deg = math.modf(value)
                    frac, mins = math.modf(self.minutes + (frac * 60))
                    sec = self.seconds + (frac * 60)

                    mins += sec // 60
                    sec %= 60

                    deg += mins // 60
                    mins %= 60

                    if deg > 180 or (180 == deg and (mins > 0 or sec > 0)):
                        raise ValueError('Latitude distance cannot be greater than 180 degrees')
                    else:
                        super().__setattr__('degrees', deg)
                        super().__setattr__('minutes', mins)
                        super().__setattr__('seconds', sec)

        elif 'minutes' == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                raise ValueError("minutes must be a numerical value") from e
            else:
                frac, mins = math.modf(value)
                secs = self.seconds + (frac * 60)
                degs = self.degrees

                if secs > 60:
                    mins += secs // 60
                    secs %= 60

                if mins >= 60:
                    degs = self.degrees + (mins // 60)
                    mins %= 60

                if degs > 180 or (180 == degs and (mins > 0 or secs > 0)):
                    raise ValueError('Latitude distance cannot be greater than 180 degrees')
                else:
                    super().__setattr__('degrees', degs)
                    super().__setattr__('minutes', mins)
                    super().__setattr__('seconds', secs)

        elif 'seconds' == key:
            try:
                secs = abs(float(value))
            except ValueError as e:
                raise ValueError("seconds must be a numerical value") from e
            else:
                mins = self.minutes
                degs = self.degrees
                if secs > 60:
                    mins = self.minutes + (value // 60)
                    secs %= 60

                if mins > 60:
                    degs = self.degrees + (mins // 60)
                    mins %= 60

                if degs > 180 or (180 == degs and (mins > 0 or secs > 0)):
                    raise ValueError('Latitude distance cannot be greater than 180 degrees')
                else:
                    super().__setattr__('degrees', degs)
                    super().__setattr__('minutes', mins)
                    super().__setattr__('seconds', secs)

        else:
            super().__setattr__(key, value)

    def __str__(self):
        if 0 == self.degrees and 0 == self.minutes and 0 == self.seconds:
            return '{}° {}\' {}" {}'.format(int(self.degrees), int(self.minutes), round(self.seconds, 2), 'N/S')
        else:
            return '{}° {}\' {}" {}'.format(int(self.degrees), int(self.minutes), round(self.seconds, 2), self.sign)

    def __float__(self):
        value = self.degrees + (self.minutes / 60) + (self.seconds / 3600)
        return value if self.sign == 'N' else value * -1

    def __add__(self, other):
        """
        Method that permits to sum a LatitudeDistance with Latitude, LatitudeDistance or tuple like (degrees, minutes
        seconds, sign). Methods returns always a LatitudeDistance object
        :param other: LatitudeDistance obj or tuple that will be interpreted like a LatitudeDistance obj
        :return: LatitudeDistance type
        """
        if type(self) == type(other):
            return float_to_latitude_distance(float(other) + float(self))

        elif type(other) == Latitude:
            return float_to_latitude_distance(float(other) + float(self))

        elif type(other) == tuple:
            if len(other) != 4:
                raise TypeError('tuple must be like (degrees, minutes, seconds, sing)')
            else:
                try:
                    a, b, c, d = abs(float(other[0])), abs(float(other[1])), abs(float(other[2])), str(other[3])
                except (ValueError, IndexError) as e:
                    raise ValueError('tuple must be like (degrees, minutes, seconds, sing)') from e
                else:
                    if d != 'N' and d != 'S':
                        raise ValueError('Sign must be N north or S south')
                    other = a + b / 60 + c / 3600 if 'N' == d else (a + b / 60 + c / 3600) * -1
                    return float_to_latitude_distance(float(self) + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """
        Method that permits to subtract Latitude or LatitudeDistance or tuple of type (degrees, minutes, secons, sign)
        to self obj.
        :param other: Latitude or LatitudeDistance or tuple object
        :return: LatitudeDistance object
        """
        if type(other) == type(self):
            return float_to_latitude_distance(float(self) - float(other))

        elif type(other) == Latitude:
            return float_to_latitude_distance(float(self) - float(other))

        elif type(other) == tuple:
            if len(other) != 4:
                raise TypeError('tuple must be like (degrees, minutes, seconds, sing)')
            else:
                try:
                    a, b, c, d = abs(float(other[0])), abs(float(other[1])), abs(float(other[2])), str(other[3])
                except (ValueError, IndexError) as e:
                    raise ValueError('tuple must be like (degrees, minutes, seconds, sing)') from e
                else:
                    if d != 'N' and d != 'S':
                        raise ValueError('Sign must be N north or S south')
                    other = a + b / 60 + c / 3600 if 'N' == d else (a + b / 60 + c / 3600) * -1
                    return float_to_latitude_distance(float(self) - other)

    def __rsub__(self, other):
        if type(other) == tuple:
            if len(other) != 4:
                raise TypeError('tuple must be like (degrees, minutes, seconds, sing)')
            else:
                try:
                    a, b, c, d = abs(float(other[0])), abs(float(other[1])), abs(float(other[2])), str(other[3])
                except (ValueError, IndexError) as e:
                    raise ValueError('tuple must be like (degrees, minutes, seconds, sing)') from e
                else:
                    return LatitudeDistance((a, b, c, d)).__sub__(self)


def float_to_latitude(value: float = 0.0) -> Latitude:
    """
    function that return a Latitude object starting from a float value
    :param value:
    :return:
    """
    try:
        value = float(value)
    except ValueError as e:
        raise ValueError('value must be a numerical value') from e
    else:
        sign = 'N' if value >= 0 else 'S'

        return Latitude(degrees=abs(value), sign=sign)


def float_to_latitude_distance(value: float = 0.0) -> LatitudeDistance:
    """
    function that returns the LatitudeDistance value starting from a float value
    :param value:
    :return:
    """
    try:
        value = float(value)
    except ValueError as e:
        raise ValueError('value must be a numerical value') from e
    else:
        sign = 'N' if value >= 0 else 'S'

        return LatitudeDistance((value, 0, 0, sign))


def meridional_part(latitude: Latitude) -> float:
    """
    this function return the meridional part of a Latitude object
    :param latitude: Latitude object
    :return: float value of meridional part
    """
    if type(latitude) != Latitude:
        raise TypeError('cannot make meridional part from {} the argument must be Latitude'.format(type(latitude)))
    # variables:
    sign = latitude.sign
    latitude = math.radians(abs(float(latitude)))

    # constants:
    briggs_log_module = 0.43429
    eccentricity_2 = 0.00672

    # variables and logic operation:
    first = 10800 / (math.pi * briggs_log_module) * \
        math.log(math.tan(math.radians(45) + (latitude / 2)), 10)

    second = (10800 / math.pi) * (eccentricity_2 * math.sin(latitude) + (1 / 3) *
                                  (eccentricity_2 ** 2) * (math.sin(latitude) ** 3) + (1 / 5) *
                                  (eccentricity_2 ** 4) * (math.sin(latitude) ** 5))

    return round(first - second, 1) if 'N' == sign else round(first - second, 1) * -1
