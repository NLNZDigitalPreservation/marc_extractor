import os

from nose.tools import *
from marc_extractor.epub import epub_to_marc
from marc_extractor.nlnz_epub import nlnz_epub_to_marc

def setup():
	print("SETUP!")

def teardown():
	print("TEAR DOWN!")

def test_basic():
	print("I ran!")

def test_epub_to_marc():
	marc = epub_to_marc(os.path.join('tests', 'data',
		'windows_party_webkit_firefox_ie.epub'))

def test_epub_to_nlnz_marc():
	marc = nlnz_epub_to_marc(os.path.join('tests', 'data',
		'windows_party_webkit_firefox_ie.epub'))

def test_epub_to_marc_with_specified_conf_file():
	marc = epub_to_marc('tests/data/windows_party_webkit_firefox_ie.epub', 
		conf_file=os.path.join('tests', 'data', 'test.conf'))