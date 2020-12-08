# -*- coding: utf-8 -*-
"""Test schema_catalog-module."""
import pytest

import lxml.etree as ET

from xml_helpers.schema_catalog import parse_catalog_schema_uris
import xml_helpers.schema_catalog


@pytest.mark.parametrize(('rewrite_rules', 'next_catalogs'), [
    ({'http://localhost.test/non-existing.xsd': 'definitely-non-existing.xsd'},
     None),
    (None, ['does/not/exist.xml', 'non/existing/file.xml']),
    ({'http://localhost.test/non-existing.xsd': 'definitely-non-existing.xsd',
      'http://localhost.test/no/schema.xsd': 'no-schema.xsd'},
     ['does/not/exist.xml', 'non/existing/file.xml']),
], ids=['With rewrite urls only',
        'With next catalogs only',
        'With both'])
def test_construct_catalog_xml(tmpdir, rewrite_rules, next_catalogs):
    """Tests that the catalog has been constructed correctly."""
    filename = tmpdir.mkdir('test').join('foo.xml')
    base_dir = tmpdir.mkdir('base_catalog')
    catalog = xml_helpers.schema_catalog.construct_catalog_xml(
        base_path=base_dir.strpath,
        rewrite_rules=rewrite_rules,
        next_catalogs=next_catalogs)
    with open(filename.strpath, 'w') as in_file:
        catalog.write(in_file)

    with open(filename.strpath) as out_file:
        tree = ET.fromstring(out_file.read())

    for key in tree.attrib:
        if key.endswith('base'):
            assert tree.attrib[key].rstrip('/') == base_dir.strpath

    rewrite_length = len(rewrite_rules) if rewrite_rules else 0
    catalog_length = len(next_catalogs) if next_catalogs else 0
    assert len(tree) == rewrite_length + catalog_length
    for element in tree:
        if 'rewriteURI' in element.tag:
            assert element.attrib['rewritePrefix'] == rewrite_rules[
                element.attrib['uriStartString']]
            # Remove the entry from the parameter to signify that we've
            # evaluated it.
            del rewrite_rules[element.attrib['uriStartString']]
        if 'nextCatalog' in element.tag:
            assert element.attrib['catalog'] in next_catalogs
            # Remove the entry from the parameter to signify that we've
            # evaluated it.
            next_catalogs.remove(element.attrib['catalog'])

    # These two parameters have to be Falsey at the end of the test.
    assert not rewrite_rules
    assert not next_catalogs


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
