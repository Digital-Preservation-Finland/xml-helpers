"""Utility functions for handling XML data with xml.etree.ElementTree data
structures"""


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
