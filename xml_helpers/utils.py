"""Utility functions for handling XML data with lxml.etree data
structures"""

import datetime
import lxml.etree as ET


XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'


def readfile(filename):
    """Read file, remove blanks and comments"""
    xmlparser = ET.XMLParser(remove_blank_text=True, remove_comments=True)
    return ET.parse(filename, parser=xmlparser)


def serialize(root_element):
    """Serialize lxml.etree structure.

    :root_element: Starting element to serialize
    :returns: Serialized XML as string

    """
    ET.cleanup_namespaces(root_element)
    return ET.tostring(root_element, pretty_print=True,
                       xml_declaration=True, encoding='UTF-8')


def get_namespace(elem):
    """return xml element's namespace"""
    return elem.nsmap[elem.prefix]


def xml_datetime(date_value):
    """Converts a python datetime to premis xml datetime."""

    if isinstance(date_value, datetime.datetime):
        return date_value.isoformat()
    else:
        return date_value


def xsi_ns(tag):
    """Prefix ElementTree tags with XSI namespace.

    object -> {http://..}object

    :tag: Tag name as string
    :returns: Prefixed tag

    """
    return '{%s}%s' % (XSI_NS, tag)


def compare_trees(tree1, tree2):
    """Compare two XML trees with ignoring whitespaces

    :tree1: Root element of lxml.etree
    :tree2: Root element of lxml.etree
    :returns: True if trees match, otherwise False
    """
    if tree1.tag.strip() != tree2.tag.strip(): return False
    if tree1.text is not None:
        if tree2.text is None: return False
        if tree1.text.strip() != tree2.text.strip(): return False
    else:
        if tree2.text is not None: return False
    if tree1.tail is not None:
        if tree2.tail is None: return False
        if tree1.tail.strip() != tree2.tail.strip(): return False
    else:
        if tree2.tail is not None: return False
    if set(tree1.attrib.keys()) != set(tree2.attrib.keys()): return False
    for attr_key, attr_value in tree1.attrib.iteritems():
        if attr_value is not None:
            if attr_key not in tree2.attrib: return False
            if attr_value.strip() != tree2.attrib[attr_key].strip(): return False
        else:
            if attr_key in tree2.attrib: return False
    if len(tree1) != len(tree2): return False
    return all(compare_trees(c1, c2) for c1, c2 in zip(tree1, tree2))


def decode_utf8(text):
    """Change UTF-8 encoded ASCII to Unicode.
    Return input unchanged, if Unicode given.

    :text: ASCII or Unicode string
    :returns: Unicode string
    """
    if not isinstance(text, unicode):
        text = text.decode('utf-8')
    return text


def encode_utf8(text):
    """Change Unicode to UTF-8 encoded ASCII.
    Return input unchanged, if ASCII given.

    :text: Unicode or ASCII string
    :returns: ASCII string
    """
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    return text

