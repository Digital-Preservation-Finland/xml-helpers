"""Install xml-helpers"""

import re
from setuptools import setup, find_packages

with open('xml_helpers/__init__.py', 'r') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


def main():
    """Install xml-helpers"""
    setup(
        name='xml_helpers',
        packages=find_packages(exclude=['tests', 'tests.*']),
        include_package_data=True,
        version=version,
        install_requires=['lxml', 'six']
    )


if __name__ == '__main__':
    main()
