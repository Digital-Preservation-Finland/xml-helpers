"""Utility functions for handling XML data with lxml.etree data
structures

Couple of functions have been adapted from a MIT licensed open source solution:

Copyright (c) 2018 Benjamin Peterson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import unicode_literals

import datetime
import os

import lxml.etree as ET
import six

CATALOG_TEMPLATE = b"""<!DOCTYPE catalog PUBLIC "-//OASIS//DTD XML Catalogs V1.0//EN" "catalog.dtd">
<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog" prefer="public" xml:base="./">
</catalog>
"""
XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'


def readfile(filename):
    """Read file, remove blanks and comments"""
    xmlparser = ET.XMLParser(remove_blank_text=True, remove_comments=True)
    return ET.parse(filename, parser=xmlparser)


def serialize(root_element):
    """Serialize lxml.etree structure.

    :root_element: Starting element to serialize
    :returns: Serialized XML as byte string

    """
    ET.cleanup_namespaces(root_element)
    return ET.tostring(
        root_element, pretty_print=True, xml_declaration=True,
        encoding='UTF-8'
    )


def get_namespace(elem):
    """return xml element's namespace"""
    return elem.nsmap[elem.prefix]


def xml_datetime(date_value):
    """Converts a python datetime to premis xml datetime."""
    if isinstance(date_value, datetime.datetime):
        return date_value.isoformat()
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
    if set(tree1.attrib.keys()) != set(tree2.attrib.keys()) or (
            len(tree1) != len(tree2)):
        return False

    for attr in ('tag', 'text', 'tail'):
        attr1_val = getattr(tree1, attr)
        attr2_val = getattr(tree2, attr)
        try:
            if attr1_val.strip() != attr2_val.strip():
                return False
        except AttributeError:
            # AttributeError takes place if None value is being stripped.
            if attr1_val != attr2_val:
                return False

    for attr_key, attr_value in tree1.attrib.iteritems():
        if attr_value.strip() != tree2.attrib[attr_key].strip():
            return False

    return all(compare_trees(c1, c2) for c1, c2 in zip(tree1, tree2))


def construct_temporary_catalog_xml(filename,
                                    base_path,
                                    rewrite_rules):
    """Constructs a catalog file filled with given base path and rewrite rules.

    :param filename: Filename to create with.
    :param base_path: The base path of the catalog. Expected to be directory.
    :param rewrite_rules: Additional rewrite rules are expected to be in dict
        format::

        {
            rewrite_uri_start_string: rewrite_uri_rewrite_prefix
        }
    :returns: Absolute filepath of the created catalog. None if no catalog
        entries were written.
    """
    parser = ET.XMLParser(dtd_validation=False, no_network=True)
    catalog_tree = ET.XML(CATALOG_TEMPLATE, parser)
    entry_added = False
    for start_string in rewrite_rules:
        rewrite_prefix = rewrite_rules[start_string]
        rewrite_element = ET.Element("rewriteURI")
        rewrite_element.attrib["uriStartString"] = start_string
        rewrite_element.attrib["rewritePrefix"] = rewrite_prefix
        catalog_tree.append(rewrite_element)
        entry_added = True

    if not entry_added:
        return None

    # We'll set absolute path to the catalog's xml:base and making sure
    # that it'll end with one ending slash.
    for key in catalog_tree.attrib:
        if key.endswith('base'):
            catalog_tree.attrib[key] = os.path.abspath(base_path).rstrip(
                '/') + '/'
            break

    elem_tree = ET.ElementTree(catalog_tree)
    elem_tree.write(filename)
    return os.path.abspath(filename)


def decode_utf8(text):
    """Change UTF-8 encoded ASCII to Unicode.
    Return input unchanged, if Unicode given.

    :text: ASCII or Unicode string
    :returns: Unicode string
    """
    if isinstance(text, six.binary_type):
        return text.decode("utf-8")
    elif isinstance(text, six.text_type):
        return text
    else:
        raise TypeError("Expected a (byte) string, got {}".format(type(text)))


def encode_utf8(text):
    """Change Unicode to UTF-8 encoded ASCII.
    Return input unchanged, if ASCII given.

    :text: Unicode or ASCII string
    :returns: ASCII byte string
    """
    if isinstance(text, six.text_type):
        return text.encode("utf-8")
    elif isinstance(text, six.binary_type):
        return text
    else:
        raise TypeError("Expected a (byte) string, got {}".format(type(text)))


def _ensure_text(s, encoding='utf-8', errors='strict'):
    """Coerce *s* to six.text_type.

    For Python 2:
      - `unicode` -> `unicode`
      - `str` -> `unicode`

    For Python 3:
      - `str` -> `str`
      - `bytes` -> decoded to `str`

    Adapted from release 1.12 under MIT license::

        https://github.com/benjaminp/six/blob/master/six.py#L892

    Copyright (c) 2018 Benjamin Peterson
    """
    if isinstance(s, six.binary_type):
        return s.decode(encoding, errors)
    elif isinstance(s, six.text_type):
        return s
    else:
        raise TypeError("not expecting type '%s'" % type(s))


def _ensure_str(s, encoding='utf-8', errors='strict'):
    """Coerce *s* to `str`.

    For Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`

    For Python 3:
      - `str` -> `str`
      - `bytes` -> decoded to `str`

    Adapted from release 1.12 under MIT license::

        https://github.com/benjaminp/six/blob/master/six.py#L892

    Copyright (c) 2018 Benjamin Peterson
    """
    if not isinstance(s, (six.text_type, six.binary_type)):
        raise TypeError("not expecting type '%s'" % type(s))
    if six.PY2 and isinstance(s, six.text_type):
        s = s.encode(encoding, errors)
    elif six.PY3 and isinstance(s, six.binary_type):
        s = s.decode(encoding, errors)
    return s
