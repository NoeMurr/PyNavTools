import math


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

        # to avoid warnings I define the attributes with self
        self.degrees = 0.0
        self.minutes = 0.0
        self.seconds = 0.0

        self.sign = sign

        self.degrees += degrees
        self.minutes += minutes
        self.seconds += seconds

    def __setattr__(self, key, value):
        """ Assign operator for checking variable """

        if "sign" == key:
            # checking sign
            try:
                value = str(value)
            except ValueError as e:
                raise ValueError("Sign must be a string E (East) or W (West)") from e
            else:
                if "E" == value:
                    super().__setattr__(key, value)
                elif "W" == value:
                    super().__setattr__(key, value)
                else:
                    raise ValueError("Sign must be a string E (East) or W (West)")

        # checking degrees value
        elif "degrees" == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                raise ValueError("degrees must be a numerical value") from e
            else:
                if value > 180:
                    raise ValueError("Longitude cannot be greater than 180 degrees")
                elif 180 == value and (self.minutes > 0 or self.seconds > 0):
                    raise ValueError("Longitude cannot be greater than 180 degrees")
                else:
                    frac, deg = math.modf(value)
                    frac, minutes = math.modf(self.minutes + (frac * 60))

                    sec = self.seconds + (frac * 60)

                    minutes += sec // 60
                    sec %= 60

                    deg += minutes // 60
                    minutes %= 60

                    if deg > 180 or (deg == 180 and (minutes > 0 or sec > 0)):
                        raise ValueError("Longitude cannot be greater than 180 degrees")

                    super().__setattr__('minutes', minutes)
                    super().__setattr__('seconds', sec)
                    super().__setattr__('degrees', deg)

        # checking minutes value
        elif "minutes" == key:
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

                if degs > 180 or (180 == degs and (mins > 0 or value > 0)):
                    raise ValueError("Longitude cannot be greater than 180 degrees")
                else:
                    super().__setattr__('degrees', degs)
                    super().__setattr__('minutes', mins)
                    super().__setattr__('seconds', value)

        # if I don't care about the value I'll set it
        else:
            super().__setattr__(key, value)

    def __str__(self):
        if 180 == self.degrees and 0 == self.minutes and 0 == self.seconds:
            return "{}° {}' {}\" {}".format(int(self.degrees), int(self.minutes), round(self.seconds, 2), 'E/W')
        elif 0 == self.degrees and 0 == self.minutes and 0 == self.seconds:
            return "{}° {}' {}\" {}".format(int(self.degrees), int(self.minutes), round(self.seconds, 2), 'E/W')
        else:
            return "{}° {}' {}\" {}".format(int(self.degrees), int(self.minutes), round(self.seconds, 2), self.sign)

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
                a = abs(float(other[0]))
                b = abs(float(other[1]))
                c = abs(float(other[2]))
                d = str(other[3])
            except ValueError as e:
                raise ValueError('the tuple must be like: '
                                 '(degrees: float, minutes: float, seconds: float, sign: str)') from e
            else:
                other = LongitudeDistance((a, b, c, d))
                return self.__add__(other)
        elif type(other) == LongitudeDistance:
            result = float(self) + float(other)
            return float_to_longitude(result)

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
                a = abs(float(other[0]))
                b = abs(float(other[1]))
                c = abs(float(other[2]))
                d = str(other[3])
            except ValueError as e:
                raise ValueError('the tuple must be like:'
                                 ' (degrees: float, minutes: float, seconds: float, sign: str)') from e
            return LongitudeDistance(Longitude(a, b, c, d), self)

        elif type(other) == LongitudeDistance:
            result = float(self) - float(other)
            return float_to_longitude(result)

        else:
            if type(other) == tuple:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                raise TypeError("Cannot subtract Longitude with {}".format(type(other)))

    def __rsub__(self, other):
        if type(other) == tuple and 4 == len(other):
            try:
                a = abs(float(other[0]))
                b = abs(float(other[1]))
                c = abs(float(other[2]))
                d = str(other[3])
            except ValueError as e:
                raise ValueError('the tuple must be like:'
                                 ' (degrees: float, minutes: float, seconds: float, sign: str)') from e
            return Longitude(a, b, c, d).__sub__(self)

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
    def __init__(self, a=(0, 0, 0, 'E'), b=None):
        self.__dict__['degrees'] = 0.0
        self.__dict__['minutes'] = 0.0
        self.__dict__['seconds'] = 0.0
        self.__dict__['sign'] = 'E'
        self.degrees = 0.0
        self.minutes = 0.0
        self.seconds = 0.0
        self.sign = 'E'
        if type(a) == Longitude and type(b) == Longitude:
            value = float(b) - float(a)
            self.sign = 'E' if value > 0 else 'W'
            value = abs(value)
            if value > 180:
                value = 360 - value
                self.sign = 'E' if 'W' == self.sign else 'E'
            self.degrees = value

        elif type(a) == Longitude and type(b) == tuple:
            if len(b) != 4:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                try:
                    deg = abs(float(b[0]))
                    mins = abs(float(b[1]))
                    sec = abs(float(b[2]))
                    sign = str(b[3])
                except ValueError as e:
                    raise ValueError('the tuple must be like:'
                                     ' (degrees: float, minutes: float, seconds: float, sign: str)') from e
                else:
                    b = deg + mins / 60 + sec / 3600 if 'E' == sign else (deg + mins / 60 + sec / 3600) * -1
                    value = b - float(a)
                    self.sign = 'E' if value > 0 else 'W'
                    value = abs(value)
                    if value > 180:
                        value = 360 - value
                        self.sign = 'E' if 'W' == self.sign else 'E'
                    self.deg = int(value)

        elif type(a) == tuple and type(b) == Longitude:
            if len(a) != 4:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                try:
                    deg = abs(float(a[0]))
                    mins = abs(float(a[1]))
                    sec = abs(float(a[2]))
                    sign = str(b[3])
                except ValueError as e:
                    raise ValueError('the tuple must be like: '
                                     '(degrees: float, minutes: float, seconds: float, sign: str)') from e
                else:
                    a = deg + mins / 60 + sec / 3600 if 'E' == sign else (deg + mins / 60 + sec / 3600)*-1
                    value = float(b) - a
                    self.sign = 'E' if value > 0 else 'W'
                    value = abs(value)
                    if value > 180:
                        value = 360 - value
                        self.sign = 'E' if 'W' == self.sign else 'E'
                    self.deg = int(value)

        elif type(a) == tuple and type(b) == tuple:
            if len(a) != 4 or len(b) != 4:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                try:
                    a_deg = abs(float(a[0]))
                    a_min = abs(float(a[1]))
                    a_sec = abs(float(a[2]))
                    a_sign = str(b[3])
                    b_deg = abs(float(b[0]))
                    b_min = abs(float(b[1]))
                    b_sec = abs(float(b[2]))
                    b_sign = str(b[3])
                except ValueError as e:
                    raise ValueError('the tuple must be like: '
                                     '(degrees: float, minutes: float, seconds: float, sign: str)') from e
                else:
                    a = a_deg + a_min / 60 + a_sec / 3600 if 'E' == a_sign else (a_deg + a_min / 60 + a_sec / 3600) * -1
                    b = b_deg + b_min / 60 + b_sec / 3600 if 'E' == b_sign else (b_deg + b_min / 60 + b_sec / 3600) * -1
                    value = b - a
                    self.sign = 'E' if value > 0 else 'W'
                    value = abs(value)
                    if value > 180:
                        value = 360 - value
                        self.sign = 'E' if 'W' == self.sign else 'E'
                    self.deg = int(value)

        elif type(a) == tuple and (b is None):
            if len(a) != 4:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                try:
                    deg = abs(float(a[0]))
                    mins = abs(float(a[1]))
                    sec = abs(float(a[2]))
                    sign = str(a[3])
                except ValueError as e:
                    raise ValueError('the tuple must be like:'
                                     ' (degrees: float, minutes: float, seconds: float, sign: str)') from e
                else:
                    self.degrees += deg
                    self.minutes += mins
                    self.seconds += sec
                    self.sign = sign

        else:
            raise TypeError("Cannot make a LongitudeDistance between {} and {}".format(type(a), type(b)))

    def __setattr__(self, key, value):
        if "sign" == key:
            # checking sign
            try:
                value = str(value)
            except ValueError as e:
                raise ValueError("Sign must be a string E (East) or W (West)") from e
            else:
                if value != 'E' and value != 'W':
                    raise ValueError("Sign must be a string E (East) or W (West)")
                else:
                    super().__setattr__(key, value)

        elif "degrees" == key:
            try:
                value = abs(float(value))
            except ValueError as e:
                raise ValueError("degrees must be a numerical value") from e
            else:
                value %= 360
                if 360 == value and (self.minutes > 0 or self.seconds > 0):
                    value = value + self.minutes / 60 + self.seconds / 3600
                    value = 360 - value
                    super().__setattr__("degrees", float(int(value)))
                    super().__setattr__("minutes", float(int((value - self.degrees) * 60)))
                    super().__setattr__("seconds", float((((value - self.degrees) * 60) - self.minutes) * 60))
                else:
                    frac, deg = math.modf(value)
                    frac, minutes = math.modf(self.minutes + (frac * 60))

                    sec = self.seconds + (frac * 60)

                    minutes += sec // 60
                    sec %= 60

                    deg += minutes // 60
                    minutes %= 60

                    if deg > 360 or (deg == 360 and (minutes > 0 or sec > 0)):
                        value = deg + minutes / 60 + sec / 3600
                        value = 360 - value
                        super().__setattr__("degrees", float(int(value)))
                        super().__setattr__("minutes", float(int((value - self.degrees) * 60)))
                        super().__setattr__("seconds", float((((value - self.degrees) * 60) - self.minutes) * 60))
                    else:
                        super().__setattr__('degrees', deg)
                        super().__setattr__('minutes', minutes)
                        super().__setattr__('seconds', sec)

        elif "minutes" == key:
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

                if degs > 360 or (360 == degs and (mins > 0 or secs > 0)):
                    value = degs + mins / 60 + secs / 3600
                    value = 360 - value
                    frac, degs = math.modf(value)
                    frac, mins = math.modf(frac * 60)
                    secs = frac * 60

                super().__setattr__('degrees', degs)
                super().__setattr__('minutes', mins)
                super().__setattr__('seconds', secs)

        elif "seconds" == key:
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

                if degs > 360 or (360 == degs and (mins > 0 or secs > 0)):
                    value = degs + mins / 60 + secs / 3600
                    value = 360 - value
                    frac, degs = math.modf(value)
                    frac, mins = math.modf(frac * 60)
                    secs = frac * 60
                    self.sign = 'E' if self.sign == 'W' else 'W'

                super().__setattr__('degrees', degs)
                super().__setattr__('minutes', mins)
                super().__setattr__('seconds', secs)

        else:
            super().__setattr__(key, value)

    def __add__(self, other):
        """
        Method that permits to sum the object LongitudeDistance with an object of Longitude or LongitudeDistance or
        a tuple of type (degrees, minutes, seconds, sign). In every case the method returns a LongitudeDistance value
        :param other: LongitudeDistance obj or tuple that will be interpreted like a LongitudeDistance obj
        :return: Longitude type
        """
        if type(other) == type(self):
            a = float(self)
            b = float(other)
            value = a + b

            return float_to_longitude_distance(value)

        elif type(other) == tuple:
            if len(other) == 4:
                try:
                    deg = float(other[0])
                    mins = float(other[1])
                    secs = float(other[2])
                    sign = str(other[3])
                except ValueError as e:
                    raise ValueError('tuple must be of type (degrees, minutes, seconds, sign)') from e
                else:
                    if sign == 'E' or sign == 'W':
                        a = float(self)
                        b = deg + mins/60 + secs / 3600 if 'E' == sign else (deg + mins/60 + secs / 3600) * -1

                        return float_to_longitude_distance(a + b)
                    else:
                        raise ValueError('sign of tuple must be E or W')
            else:
                raise ValueError('tuple must be of type (degrees, minutes, seconds, sign)')

        elif type(other) == Longitude:
            a = float(self)
            b = float(other)
            value = a + b

            return float_to_longitude_distance(value)

        else:
            raise TypeError("cannot sum {} with {}".format(type(self), type(other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """
        Method that permits to subtract a Longitude or LongitudeDistance or tuple object to self object.
        the returned type is always a LongitudeDistance object.
        :param other: Longitude or LongitudeDistance or tuple object
        :return: LongitudeDistance object
        """
        if type(other) == type(self):
            a = float(self)
            b = float(other)
            return float_to_longitude_distance(a - b)

        elif type(other) == tuple:
            if len(other) == 4:
                try:
                    deg = float(other[0])
                    mins = float(other[1])
                    secs = float(other[2])
                    sign = str(other[3])
                except ValueError as e:
                    raise ValueError('tuple must be of type (degrees, minutes, seconds, sign)') from e
                else:
                    a = float(self)
                    b = deg + mins / 60 + secs / 3600 if 'E' == sign else (deg + mins / 60 + secs / 3600) * -1

                    return float_to_longitude_distance(a - b)
            else:
                raise ValueError('tuple must be like (degrees, minutes, seconds,sign)')

        elif type(other) == Longitude:
            a = float(self)
            b = float(other)

            return float_to_longitude_distance(a - b)

        else:
            raise TypeError("cannot sub {} with {}".format(type(self), type(other)))

    def __rsub__(self, other):
        if type(other) == tuple and len(other) != 4:
            b = self
            a = LongitudeDistance(other)

            return a - b
        else:
            raise TypeError("cannot rsub {} with {}".format(type(self), type(other)))

    def __str__(self):
        return "{}° {}' {}\" {}".format(int(self.degrees), int(self.minutes), round(self.seconds, 2), self.sign)

    def __float__(self):
        value = self.degrees + (self.minutes / 60) + (self.seconds / 3600)
        value = value if self.sign == 'E' else value * -1
        return value


def float_to_longitude(x: float = 0.0) -> Longitude:
    try:
        x = float(x)
    except ValueError as e:
        raise ValueError("Cannot make a Longitude without a numerical value") from e
    else:
        if x < 0:
            sign = 'W'
        else:
            sign = 'E'

        return Longitude(degrees=abs(x), sign=sign)


def float_to_longitude_distance(x: float = 0.0) -> LongitudeDistance:
    try:
        x = float(x)
    except ValueError as e:
        raise ValueError("Cannot make a LongitudeDistance without a numerical value") from e
    else:
        if x < 0:
            sign = 'W'
        else:
            sign = 'E'
        return LongitudeDistance((x, 0, 0, sign))
