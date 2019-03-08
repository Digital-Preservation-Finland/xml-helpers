"""Test for XML utils"""

import lxml.etree as ET
import xml_helpers.utils as u


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
