##############################################################################
#
# @author:  Noè Murr
# @file:    Longitude.py
# @brief:   contains the definition of Longitude class.
#
##############################################################################


class Longitude:
    """ Simple class representing the concept of Navigational longitude """

    def __init__(self, degrees, minutes, seconds, sign):
        """ Constructor for the class """

        # checking sign
        try:
            sign = str(sign)
        except ValueError:
            raise ValueError("Sign must be a string E (East) or W (West)")
        else:
            if str(sign) != 'E' or str(sign) != 'W':
                raise ValueError("Sign must beE (East) or W (West)")
            else:
                self.sign = sign

        # checking degrees
        try:
            degrees = abs(float(degrees))
            minutes = abs(float(minutes))
            seconds = abs(float(seconds))
        except ValueError:
            raise ValueError("Degrees, minutes and seconds must be numerical value")
        else:
            # first check
            self.degrees = int(degrees)
            minutes += (degrees - int(degrees)) * 60

            self.minutes = int(minutes)
            seconds += (minutes - int(minutes)) * 60

            self.seconds = seconds

            # second check
            if self.seconds >= 60:
                self.minutes += self.seconds // 60
                self.seconds %= 60

            if self.minutes >= 60:
                self.degrees += self.minutes // 60
                self.minutes %= 60

            if self.degrees > 180:
                raise ValueError("Longitude cannot be greater than 180 degrees")
            elif self.degrees == 180 and self.minutes != 0 and self.seconds != 0:
                raise ValueError("Longitude cannot be greater than 180 degrees")

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
                if str(value) != 'E' or str(value) != 'W':
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
                    deg = int(value)
                    minutes = self.minutes + ((value - int(value)) * 60)

                    sec = self.seconds + ((minutes - int(minutes)) * 60)
                    minutes = int(minutes)

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
                mins = int(value)
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
