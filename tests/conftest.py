"""Fixtures to be used for unit testing."""

import os
import pytest


@pytest.fixture(scope='session')
def utf8_file():
    """Returns XML file path with UTF-8 set as charset."""
    return os.path.join(os.path.dirname(__file__), 'data', 'utf8_file.xml')


@pytest.fixture(scope='session')
def compare_tree_xml():
    """Provides a class that has a collection of various XML content."""
    return CompareTrees


class CompareTrees:
    """To contain various different XML-content for testing purposes."""

    @classmethod
    def base(cls):
        """Base XML to be compared with."""
        return b"""<?xml version="1.0" encoding="UTF-8" ?>
<root>
    <child number="1" plus-one="2">A</child>
    <child number="2" plus-one="3">B</child>
</root>"""

    @classmethod
    def child_incorrect_attrib(cls):
        """Base that has a childelement with incorrect attribute."""
        return b"""<?xml version="1.0" encoding="UTF-8" ?>
<root>
    <child number="1" plus-one="2">A</child>
    <child number="2" plus-one="2">B</child>
</root>"""

    @classmethod
    def extra_attrib(cls):
        """Base that has an additional attribute."""
        return b"""<?xml version="1.0" encoding="UTF-8" ?>
<root version="fail">
    <child number="1" plus-one="2">A</child>
    <child number="2" plus-one="3">B</child>
</root>"""

    @classmethod
    def extra_element(cls):
        """Base that has an extra element."""
        return b"""<?xml version="1.0" encoding="UTF-8" ?>
<root>
    <child number="1" plus-one="2">A</child>
    <child number="2" plus-one="3">B</child>
    <child number="3" plus-one="4">C</child>
</root>"""

    @classmethod
    def extra_text(cls):
        """Base that has an extra text."""
        return b"""<?xml version="1.0" encoding="UTF-8" ?>
<root>
    <child number="1" plus-one="2">A</child>
    <child number="2" plus-one="3">B</child>
    Fail
</root>"""

    @classmethod
    def mixed_content(cls):
        """Base that has empty spaces padding the content and attributes
        mixed up.
        """
        return b"""<?xml version="1.0" encoding="UTF-8" ?>
<root>

    <child number="1     " plus-one="2">A                      </child>

    <child plus-one="     3" number="2">                      B</child>

</root>"""

    @classmethod
    def none_text_content(cls):
        """Base that has None for root.text."""
        return b"""<?xml version="1.0" encoding="UTF-8" ?>
<root><child number="1" plus-one="2">A</child>
    <child number="2" plus-one="3">B</child></root>"""
