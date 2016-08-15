from distutils.core import setup

__all__ = ['Latitude', 'LatitudeDistance', 'Longitude', 'LongitudeDistance', 'floattolatitude',
           'floattolatitudedistance', 'floattolongitude', 'floattolongitudedistance', 'meridionalpart']

setup(
    name='PyNavTools',
    version='0.1.0',
    author='Noè Murr',
    author_email='noe.murr@outlook.com',
    packages=['GreatCircle', 'RhumbLine'],
    scripts=['latitude.py', 'longitude.py', 'course.py', 'point.py'],
    url='https://github.com/NoeMurr/PyNavTools',
    license=open('LICENSE', 'r').read(),
    description='Simple library for navigational computing.',
    long_description=open('README.md', 'r')
)
