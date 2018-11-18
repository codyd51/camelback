from setuptools import setup

from camelback import __version__


# TODO(PT): figure out if we need njas/ prefix in package_data
setup(
    name='camelback',
    version=__version__,
    description='Convert casing styles of streams',
    url='https://github.com/codyd51/camelback',
    author='Phillip Tennen',
    packages=['camelback'],
)
