from marc_extractor.epub import epub_to_marc
from pymarc import Record, Field, MARCWriter

def nlnz_epub_to_marc(filepath):
	record = epub_to_marc(filepath)
	# Field 300
	record.add_ordered_field(Field('300', [' ', ' '], 
	    ['a', '1 online resource']))
	# Field 500
	record.add_grouped_field(Field('500', [' ', ' '], 
	    ['a', 'Archived by the National Library of New Zealand in EPUB', 
	     '5', 'Nz']),
		Field('500', [' ', ' '], 
	    ['a', 'Hypertext links contained in the archived instances of this'
	    ' title are non-functional.']),
	    Field('500', [' ', ' '], ['a', 'Machine-generated record'
	    ' from publisher-derived data.', '5', 'Nz'])
	    )
	return record