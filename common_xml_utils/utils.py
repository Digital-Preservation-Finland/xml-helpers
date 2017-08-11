"""Utility functions for handling XML data with xml.etree.ElementTree data
structures"""

import xml.etree.ElementTree as ET


def indent(elem, level=0):
    """Add indentation for the ElementTree elements

    Modifies the given element tree inplace.

    :elem: Starting element

    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def serialize(root_element, namespaces):
    """Serialize ElementTree structure with PREMIS namespace mapping.

    This modifies the default "ns0:tag" style prefixes to "premis:tag"
    prefixes.

    :element: Starting element to serialize
    :namespaces: Namespaces as dict "prefix:namespace"
    :returns: Serialized XML as string

    """
    # We can't serialize an ElementTree, so serialize the tree's
    # root Element instead
    if isinstance(root_element, ET.ElementTree):
        root_element = root_element.getroot()

    register_namespaces(namespaces)
    indent(root_element)

    return ET.tostring(root_element, encoding='utf8')


def register_namespaces(namespaces):
    """Register given namespaces
    """
    for prefix, name in namespaces.items():
        ET.register_namespace(prefix, name)

