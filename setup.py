"""
Install common-xml-utils
"""

import os
from setuptools import setup, find_packages


def scripts_list():
    """Return list of command line tools from package pas.scripts"""
    scripts = []
    for modulename in os.listdir('common_xml_utils/scripts'):
        if modulename == '__init__.py':
            continue
        if not modulename.endswith('.py'):
            continue
        modulename = modulename.replace('.py', '')
        scriptname = modulename.replace('_', '-')
        scripts.append('%s = common_xml_utils.scripts.%s:main' % (scriptname, modulename))
    print scripts
    return scripts


def main():
    """Install common-xml-utils"""
    setup(
        name='common_xml_utils',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='dev',
        entry_points={'console_scripts': scripts_list()})


if __name__ == '__main__':
    main()
