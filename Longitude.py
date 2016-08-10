##############################################################################
#
# @author:  Noè Murr
# @file:    Longitude.py
# @brief:   contains the definition of Longitude class.
#
##############################################################################


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
        # sum of two longitudes
        if type(other) == type(self):
            value = float(self) + float(other)
            sign = 'E' if value > 0 else 'W'
            value = abs(value)
            if value >= 180:
                value = 360 - value
                sign = 'E' if sign == 'W' else 'W'
            return Longitude(degrees=value, sign=sign)

        # sum with tuple of type (degs, mins, secs, sign)
        elif type(other) == tuple and 4 == len(other):
            degs, mins, secs, sign = other
            try:
                degs = abs(float(degs))
                mins = abs(float(mins))
                secs = abs(float(secs))
                sign = str(sign)
            except ValueError as e:
                e.message = 'the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)'
                raise
            return self.__add__(Longitude(degs, mins, secs, sign))
        else:
            if type(other) == tuple:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                raise TypeError("Cannot add Longitude with {}".format(type(other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        # sub of two longitudes
        if type(other) == type(self):
            value = float(self) - float(other)
            sign = 'E' if value > 0 else 'W'
            value = abs(value)
            if value >= 180:
                value = 360 - value
                sign = 'E' if sign == 'W' else 'W'
            return Longitude(degrees=value, sign=sign)

        elif type(other) == tuple and 4 == len(other):
            degs, mins, secs, sign = other
            try:
                degs = abs(float(degs))
                mins = abs(float(mins))
                secs = abs(float(secs))
                sign = str(sign)
            except ValueError as e:
                e.message = 'the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)'
                raise
            return self.__sub__(Longitude(degs, mins, secs, sign))

        else:
            if type(other) == tuple:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                raise TypeError("Cannot subtract Longitude with {}".format(type(other)))

    def __rsub__(self, other):
        if type(other) == type(self):
            return other.__sub__(self)
        elif type(other) == tuple and 4 == len(other):
            degs, mins, secs, sign = other
            try:
                degs = abs(float(degs))
                mins = abs(float(mins))
                secs = abs(float(secs))
                sign = str(sign)
            except ValueError as e:
                e.message = 'the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)'
                raise
            return Longitude(degs, mins, secs, sign).__sub__(self)

        else:
            if type(other) == tuple:
                raise TypeError('the tuple must be like: (degrees: float, minutes: float, seconds: float, sign: str)')
            else:
                raise TypeError("Cannot subtract Longitude with {}".format(type(other)))
