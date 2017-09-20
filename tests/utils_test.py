"""Test for XML utils"""

import xml.etree.ElementTree as ET
import xml_helpers.utils as u

def test_indent():
    """test indent"""
    xml = '<a><b/></a>'
    ind_xml='<a>\n  <b />\n</a>\n'
    tree = ET.fromstring(xml)
    u.indent(tree)
    assert ET.tostring(tree) == ind_xml


def test_serialize():
    """test serialize"""
    ns = {'a': 'b'}
    xml = '<a xmlns="b"><b/></a>'
    ser_xml='<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n' \
            '<a:a xmlns:a="b">\n  <a:b />\n</a:a>\n'
    result = u.serialize(ET.fromstring(xml), ns)
    assert result == ser_xml

def test_register_namespaces():
    """test register_namespaces"""
    ns_map = {'a': 'b', 'c': 'd'}
    u.register_namespaces(ns_map)

    assert ET._namespace_map['b'] == 'a'
    assert ET._namespace_map['d'] == 'c'

def test_get_namespace():
    """test get_namespace"""
    ns_map = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    u.register_namespaces(ns_map)
    elem = ET.Element(u.xsi_ns('a'))
    assert u.get_namespace(elem) == 'http://www.w3.org/2001/XMLSchema-instance'

def test_xsi_ns():
    """test xsi namespace"""
    assert u.xsi_ns('a') == '{http://www.w3.org/2001/XMLSchema-instance}a'
