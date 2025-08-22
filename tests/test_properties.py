import os
import tempfile
import textwrap

import pytest

from properties import Properties


@pytest.fixture
def temp_config_file():
    """ Create a temporty config file for testing."""
    content = textwrap.dedent ("""
        [WebsiteSection]
        website.name = TestSite 
    """ )
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.remove(f.name)

def test_get_config_returns_parser(temp_config_file):
    props = Properties(filename=temp_config_file)
    parser = props.get_config(temp_config_file)

    assert parser.has_section("WebsiteSection")
    assert parser.has_option("WebsiteSection", "website.name")
    assert parser.get("WebsiteSection", "website.name") == "TestSite"

def test_get_website_name(temp_config_file):
    props = Properties(filename=temp_config_file)
    assert props.get_website_name() == "TestSite"

def test_missing_section_or_option_raises_error(temp_config_file):
    #Overwrite file with incomplete content.
    with open(temp_config_file, "w") as f:
        f.write("[OtherSection]\nfoo=bar\n")

    props = Properties(filename=temp_config_file)

    with pytest.raises(Exception):
        props.get_website_name()