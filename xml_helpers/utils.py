"""Utility functions for handling XML data with lxml.etree data
structures"""

import lxml.etree as ET


XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'


def readfile(filename):
    """Read file, remove blanks and comments"""
    return ET.XMLParser(remove_blank_text=True, remove_comments=True)

def serialize(root_element):
    """Serialize lxml.etree structure.

    :root_element: Starting element to serialize
    :returns: Serialized XML as string

    """
    return ET.tostring(ET.cleanup_namespaces(root_element), pretty_print=True,
                       xml_declaration=True, encoding='UTF-8')


def get_namespace(elem):
    """return xml element's namespace"""
    return elem.nsmap[elem.prefix]


def xsi_ns(tag):
    """Prefix ElementTree tags with XSI namespace.

    object -> {http://..}object

    :tag: Tag name as string
    :returns: Prefixed tag

    """
    return '{%s}%s' % (XSI_NS, tag)
