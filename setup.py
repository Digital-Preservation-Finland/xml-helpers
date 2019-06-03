"""Install xml-helpers"""

from setuptools import setup, find_packages
from version import get_version


def main():
    """Install xml-helpers"""
    setup(
        name='xml_helpers',
        packages=find_packages(exclude=['tests', 'tests.*']),
        include_package_data=True,
        version=get_version(),
        install_requires=['lxml', 'six']
    )


if __name__ == '__main__':
    main()
