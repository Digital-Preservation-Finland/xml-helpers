"""
Install xml-helpers
"""

import os
from setuptools import setup, find_packages


def main():
    """Install xml-helpers"""
    setup(
        name='xml_helpers',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='0.1')


if __name__ == '__main__':
    main()
