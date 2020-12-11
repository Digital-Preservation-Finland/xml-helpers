# -*- coding: utf-8 -*-
"""Test schema_catalog-module."""
from xml_helpers.schema_catalog import parse_catalog_schema_uris


def test_parse_catalog_schema_uris():
    """Tests the parse_catalog_schema_uris function."""
    uris = parse_catalog_schema_uris('tests/data/', 'catalog_main.xml')
    assert len(uris) == 5
    assert uris['http://localhost/first_schema.xsd'] == (
        './schemas/first_schema.xsd')
    assert uris['http://secondary_host/xml.xsd'] == (
        './schemas_external/secondary_host/xml.xsd')
    assert uris['http://third_host/xml.xsd'] == (
        './schemas_external_two/third_host/xml.xsd')
