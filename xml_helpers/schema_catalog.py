# -*- coding: utf-8 -*-
"""A module containing XML catalog related operations."""
import os

import lxml.etree as ET

from xml_helpers.utils import xml_ns

# pylint: disable=E501
CATALOG_DOCTYPE = b'<!DOCTYPE catalog PUBLIC "-//OASIS//DTD XML Catalogs V1.0//EN" "catalog.dtd">'  # noqa: E501


def construct_catalog_xml(base_path='.',
                          rewrite_rules=None,
                          next_catalogs=None):
    """Constructs a catalog XML object filled with given base path and rewrite
    rules.

    For more information how the XML catalog is structured, please see
    https://xmlcatalogs.org/ .

    :param base_path: The base path of the catalog. Expected to be a directory.
    :param rewrite_rules: Rewrite entries to be added when constructing
        the catalog. Additional rewrite rules are expected to be in dict
        format that contains both the uriStartString and rewritePrefix to
        help construct rewriteURI element::

        {
            rewrite_uri_start_string: rewrite_uri_rewrite_prefix
        }

    :param next_catalogs: List of catalog filepaths that this catalog is
        expected to link to.
    :returns: ElementTree-object of the catalog with the information provided.
    """
    root = ET.Element('catalog')
    root.attrib['xmlns'] = 'urn:oasis:names:tc:entity:xmlns:xml:catalog'
    root.attrib['prefer'] = 'public'

    # We'll set absolute path to the catalog's xml:base and making sure
    # that it'll end with one ending slash.
    root.attrib[xml_ns('base')] = os.path.abspath(base_path).rstrip(
        '/') + '/'

    if rewrite_rules is not None:
        for start_string in rewrite_rules:
            rewrite_prefix = rewrite_rules[start_string]
            rewrite_element = ET.Element("rewriteURI")
            rewrite_element.attrib["uriStartString"] = start_string
            rewrite_element.attrib["rewritePrefix"] = rewrite_prefix
            root.append(rewrite_element)

    if next_catalogs is not None:
        for catalog in next_catalogs:
            catalog_element = ET.Element("nextCatalog")
            catalog_element.attrib["catalog"] = catalog
            root.append(catalog_element)

    return ET.ElementTree(root)


def parse_catalog_schema_uris(base_path, catalog_relpath, schema_uris=None):
    """Parses the schema URIs from a given schema catalog file and its
    related additional catalog entry files specified in the nextCatalog
    elements of each catalog file that is read.

    :param base_path: The base path of the catalog file location
    :param catalog_relpath: The relative path to the catalog file from
                            the base_path
    :returns: A dictionary of schema URIs with uriStartStrings and
              rewritePrefixes (including xml:base)
    """
    namespaces = {
        'catalog': 'urn:oasis:names:tc:entity:xmlns:xml:catalog',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }
    root = ET.parse(os.path.join(base_path, catalog_relpath)).getroot()

    if not schema_uris:
        schema_uris = dict()
    for rewrite_uri in root.xpath('//catalog:rewriteURI',
                                  namespaces=namespaces):

        # Add the xml:base value to the rewritePrefix path if it exists,
        # use the closest found value, starting from the current node
        try:
            xml_base = rewrite_uri.xpath(
                './ancestor-or-self::*/@xml:base', namespaces=namespaces)[-1]
        except IndexError:
            xml_base = ''

        rewrite_path = os.path.join(xml_base, rewrite_uri.get('rewritePrefix'))
        schema_uris[rewrite_uri.get('uriStartString')] = rewrite_path

    # Parse all additional catalog entry files as well, including additional
    # catalog entries listed in the subsequent catalog files that are parsed
    for next_catalog in root.xpath('//catalog:nextCatalog',
                                   namespaces=namespaces):
        next_catalog_relpath = next_catalog.get('catalog')
        schema_uris = parse_catalog_schema_uris(
            base_path=os.path.dirname(os.path.join(base_path,
                                                   next_catalog_relpath)),
            catalog_relpath=os.path.basename(next_catalog_relpath),
            schema_uris=schema_uris)

    return schema_uris
