"""
Install common-xml-utils
"""

import os
from setuptools import setup, find_packages


def main():
    """Install common-xml-utils"""
    setup(
        name='common_xml_utils',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='0.1')


if __name__ == '__main__':
    main()
