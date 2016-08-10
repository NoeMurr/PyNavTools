##############################################################################
#
# @author:  Noè Murr
# @file:    latitude.py
# @brief:   contains definition of Latitude.
#
##############################################################################


class Latitude:

    def __init__(self, degrees, minutes, seconds, sign):
        # checking sign
        try:
            sign = str(sign)
        except ValueError:
            raise ValueError("Sign must be a string N (North) or S")
        else:
            if str(sign) != 'N' or str(sign) != 'S':
                raise ValueError("Sign must be N (North) or S")
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

            if self.degrees > 90:
                raise ValueError("Latitude cannot be greater than 90 degrees")
            elif self.degrees == 90 and self.minutes != 0 and self.seconds != 0:
                raise ValueError("Latitude cannot be greater than 90 degrees")
