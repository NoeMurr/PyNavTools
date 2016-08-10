##############################################################################
#
# @author:  Noè Murr
# @file:    Longitude.py
# @brief:   contains the definition of Longitude class.
#
##############################################################################


class Longitude:
    def __init__(self, degrees, minutes, seconds, sign):
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
        elif "degrees" == key:
            try:
                value = float(value)
            except ValueError as e:
                e.message = "degrees must be a numerical value"
                raise
            else:
                super().__setattr__(key,value)

        elif "minutes" == key:
            pass
        elif "seconds" == key:
            pass
