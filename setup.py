from setuptools import find_packages
from setuptools import setup
 
setup(
    name="ParseLog",
    version="0.1",
    packages=find_packages(exclude=['tests']),
    setup_requires=['setuptools'],
)