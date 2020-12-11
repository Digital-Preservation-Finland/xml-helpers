# -*- coding: utf-8 -*-
"""A module containing XML catalog related operations."""

import os

import lxml.etree as ET


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
        schema_uris = parse_catalog_schema_uris(base_path,
                                                next_catalog_relpath,
                                                schema_uris=schema_uris)

    return schema_uris
