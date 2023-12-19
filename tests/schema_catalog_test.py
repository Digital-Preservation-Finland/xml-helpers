"""Test schema_catalog-module."""
import pytest

import lxml.etree as ET

from xml_helpers.schema_catalog import (construct_catalog_xml,
                                        parse_catalog_schema_uris)
from xml_helpers.utils import ensure_text, serialize


# pylint: disable=consider-using-dict-comprehension
@pytest.mark.parametrize(('rewrite_rules', 'next_catalogs'), [
    ({'http://localhost.test/non-existing.xsd': 'definitely-non-existing.xsd'},
     {}),
    ({}, ['does/not/exist.xml', 'non/existing/file.xml']),
    ({'http://localhost.test/non-existing.xsd': 'definitely-non-existing.xsd',
      'http://localhost.test/no/schema.xsd': 'no-schema.xsd'},
     ['does/not/exist.xml', 'non/existing/file.xml']),
    ({'http://localhost.test/nön-existing.xsd': 'definitely-nön-existing.xsd'},
     {}),
], ids=['With rewrite urls only',
        'With next catalogs only',
        'With both',
        'Rewrite urls containing diacritics'])
def test_construct_catalog_xml(tmpdir, rewrite_rules, next_catalogs):
    """Tests that the catalog has been constructed correctly."""
    filename = tmpdir.mkdir('test').join('foo.xml')
    base_dir = tmpdir.mkdir('base_catalog')
    catalog = construct_catalog_xml(base_path=base_dir.strpath,
                                    rewrite_rules=rewrite_rules,
                                    next_catalogs=next_catalogs)
    with open(filename.strpath, 'wb') as in_file:
        in_file.write(serialize(catalog))

    with open(filename.strpath, 'rb') as out_file:
        tree = ET.fromstring(out_file.read())

    for key in tree.attrib:
        if key.endswith('base'):
            assert tree.attrib[key].rstrip('/') == base_dir.strpath

    assert len(tree) == len(rewrite_rules) + len(next_catalogs)

    # Ensure that the keys and values of the input dict are text (unless it
    # is None), so that we can compare the input with the output
    decoded_rules = None
    if rewrite_rules:
        decoded_rules = {
            ensure_text(k):ensure_text(v) for k, v in rewrite_rules.items()}

    for element in tree:
        if 'rewriteURI' in element.tag:
            assert element.attrib['rewritePrefix'] == decoded_rules[
                element.attrib['uriStartString']]
            # Remove the entry from the parameter to signify that we've
            # evaluated it.
            del decoded_rules[element.attrib['uriStartString']]
        if 'nextCatalog' in element.tag:
            assert element.attrib['catalog'] in next_catalogs
            # Remove the entry from the parameter to signify that we've
            # evaluated it.
            next_catalogs.remove(element.attrib['catalog'])

    # These two parameters have to be Falsey at the end of the test.
    assert not decoded_rules
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
