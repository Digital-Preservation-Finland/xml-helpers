"""Test for XML utils"""

from datetime import datetime
import lxml.etree as ET
import pytest

import xml_helpers.utils as u


def test_readfile_utf8(utf8_file):
    """Test that it won't break reading UTF-8 charset set XML file."""
    u.readfile(utf8_file)


def test_xml_datetime():
    """Test that given datetime object is successfully converted."""
    given_date = datetime(2018, 12, 31)
    assert u.xml_datetime(given_date) != given_date


def test_xml_datetime_exception():
    """Test that given value is returned as is if it's not a datetime."""
    given_date = '2018-12-31T00:00:00'
    assert u.xml_datetime(given_date) == given_date


def test_serialize():
    """test serialize"""
    xml = '<a:x xmlns:a="b"><a:y/></a:x>'
    ser_xml = ('<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
               '<a:x xmlns:a="b">\n  <a:y/>\n</a:x>\n')
    result = u.serialize(ET.fromstring(xml))
    assert result == ser_xml


def test_get_namespace():
    """test get_namespace"""
    elem = ET.Element(u.xsi_ns('a'))
    assert u.get_namespace(elem) == 'http://www.w3.org/2001/XMLSchema-instance'


def test_xsi_ns():
    """test xsi namespace"""
    assert u.xsi_ns('a') == '{http://www.w3.org/2001/XMLSchema-instance}a'


@pytest.mark.parametrize(('xml', 'expected'), [
    ('mixed_content', True),
    ('extra_element', False),
    ('extra_attrib', False),
    ('extra_text', False),
    ('child_incorrect_attrib', False),
    ('none_text_content', False),
])
def test_compare_trees(compare_tree_xml, xml, expected):
    """Test compare_trees-function."""
    assert u.compare_trees(
        ET.fromstring(compare_tree_xml.base()),
        ET.fromstring(getattr(compare_tree_xml, xml)())
    ) == expected


@pytest.mark.parametrize('func', [
    u.decode_utf8,
    u.encode_utf8
])
def test_decode_encode_utf8_file(utf8_file, func):
    """Test that decode_utf8/encode_utf8 doesn't break."""
    with open(utf8_file, 'r') as in_file:
        func(in_file.read())

    assert func(123456789) == 123456789
