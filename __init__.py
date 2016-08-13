##############################################################################
#
# @author:  Noè Murr
# @file:    __init__.py
# @brief:   simple init file for PyNavTool module.
#
##############################################################################

# necessary modules.

# math is necessary for navigation calculation.
from distutils.core import setup

setup(
    name='PyNavTools',
    version='0.1.0',
    author='Noè Murr',
    author_email='noe.murr@outlook.com',
    packages=['GreatCircle', 'RhumbLine'],
    scripts=['latitude.py', 'longitude.py', 'course.py', 'point.py'],
    url='https://github.com/NoeMurr/PyNavTools'
)


