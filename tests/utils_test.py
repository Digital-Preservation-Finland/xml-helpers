"""Test for XML utils"""

from resource import getrusage, RUSAGE_SELF
from io import BytesIO

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
    ser_xml = (b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
               b'<a:x xmlns:a="b">\n  <a:y/>\n</a:x>\n')
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
    with open(utf8_file, 'rb') as in_file:
        func(in_file.read())


def test_decode_utf8():
    """
    Test that byte strings are decoded to Unicode,
    while Unicode strings are returned as is
    """
    assert u.decode_utf8(b't\xc3\xa4hti') == "tähti"
    assert u.decode_utf8("tähti") == "tähti"


def test_encode_utf8():
    """
    Test that Unicode strings are encoded to byte strings using UTF-8,
    while byte strings are returned as is
    """
    assert u.encode_utf8("tähti") == b't\xc3\xa4hti'
    assert u.encode_utf8(b't\xc3\xa4hti') == b't\xc3\xa4hti'


@pytest.mark.parametrize(('text', 'valid'), [
    ('test string', True),
    (b'test string', True),
    (12345, False)
])
def test_ensure_text(text, valid):
    """Tests that ensure_text() returns the expected type."""
    if valid:
        assert isinstance(u.ensure_text(text), str)
    else:
        with pytest.raises(TypeError):
            u.ensure_text(text)


def test_iter_elements_utf8_file(utf8_file):
    """Test the `iter_elements()` function"""
    elements = list(u.iter_elements(utf8_file))
    assert len(elements) == 7

    for element in elements:
        assert element.tag
        assert element.text


def test_iter_elements_rss():
    """Test memory usage is limited for the `iter_elements()` function.
    """

    xmldata = BytesIO("\n".join(
        ['<?xml version="1.0" encoding="UTF-8" ?>'] +
        ['<data>'] +
        [f'<name value="value {value}">text {value}</name>'
         for value in range(10000)] +
        ['</data>']
    ).encode("utf-8"))

    element_count = 0
    rss_before = getrusage(RUSAGE_SELF).ru_maxrss

    for element in u.iter_elements(xmldata):
        assert element.tag
        rss_usage = getrusage(RUSAGE_SELF).ru_maxrss - rss_before
        assert rss_usage < 1  # KiB
        element_count += 1

    assert element_count == 10001
