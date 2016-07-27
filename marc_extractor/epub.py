import zipfile
from lxml import etree
from pymarc import Record, Field, MARCWriter
import codecs
from imp import reload
from datetime import datetime
import configparser
import logging
import os
# import logging

PUNCTUATION = '.,!?@#$%^&*()/<> '
NON_FILING_WORDS = ('the', 'at', 'an')

copyright_year_range = []
for i in range(1900, 2150):
    copyright_year_range.append(str(i))

def _(str):
    if str == '':
        return ' '
    else:
        return str


def build_leader(leader_dict):
    leader_string = '00000%s%s%s a2200000%s%s%s4500' % (
        _(leader_dict['record_status']),
        _(leader_dict['type_of_record']),
        _(leader_dict['bibliographic_level']),
        _(leader_dict['encoding_level']),
        _(leader_dict['descriptive_cataloguing_form']),
        _(leader_dict['multipart_resource_record_level']),
        )
    return leader_string


def build_tag_005():
    "Creates a formatted date string, accurate to the nearest second."
    d = datetime.now().strftime('%Y%m%d%H%M%S.0')
    return d


def build_tag_006(tag_006_dict, tag_008_dict):
    tag_006_string = '%s    %s%s  %s        ' % (
        _(tag_006_dict['form_of_material']),
        _(tag_008_dict['target_audience']),
        _(tag_008_dict['form_of_item']),
        _(tag_006_dict['type_of_computer_file'])
        )
    return tag_006_string


def build_tag_007(tag_007_dict):
    tag_007_string = '%s%s%s%s%s%s%s%s%s%s%s' % (
        _(tag_007_dict['type_of_resource']),
        _(tag_007_dict['specific_material_designation']),
        _(tag_007_dict['color']),
        _(tag_007_dict['dimensions']),
        _(tag_007_dict['sound']),
        _(tag_007_dict['image_bit_depth']),
        _(tag_007_dict['file_formats']),
        _(tag_007_dict['quality_assurance_targets']),
        _(tag_007_dict['antecedent']),
        _(tag_007_dict['level_of_compression']),
        _(tag_007_dict['reformatting_quality']),
        )
    return tag_007_string


def build_tag_008(tag_008_dict, md_location, ns):
    creation_date = datetime.now().strftime('%y%m%d')
    date_one = '    '
    if md_location.xpath('dc:date/text()', namespaces=ns) and \
        md_location.xpath('dc:date/text()', namespaces=ns)[0] and len(
            md_location.xpath('dc:date/text()', namespaces=ns)[0]
            ) == 4:
        date_one = md_location.xpath('dc:date/text()', namespaces=ns)[0]
    tag_008_string = '%s%s%s    nz     %s%s   %s%s%s%s%s %s   %s%s%s' % (
        creation_date,
        _(tag_008_dict['publication_status']),
        date_one,
        _(tag_008_dict['target_audience']),
        _(tag_008_dict['form_of_item']),
        _(tag_008_dict['type_of_computer_file']),
        _(tag_008_dict['government_publication']),
        _(tag_008_dict['conference_publication']),
        _(tag_008_dict['festshrift']),
        _(tag_008_dict['literary_form']),
        _(tag_008_dict['index']),
        _(tag_008_dict['language']),
        _(tag_008_dict['modified_record']),
        _(tag_008_dict['cataloguing_source']),
        )
    return tag_008_string

def epub_to_marc(fname, 
    conf_file=os.path.join(os.path.dirname(os.path.realpath(__file__)),
        'epub.conf')):
    ns = {
    'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
    'pkg': 'http://www.idpf.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    for el in tree:
        for elel in el:
            for item in elel.items():
                if item[0] == 'full-path':
                    cfname = item[1]
    
    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]

    # Read from the config file
    conf = configparser.ConfigParser()
    conf.read(conf_file)
    leader_dict = {}
    tag_005_dict = {}
    tag_006_dict = {}
    tag_007_dict = {}
    tag_008_dict = {}
    tag_040_dict = {}
    tag_264_dict = {}

    sections = conf.sections()
    for section in sections:
        if section == 'leader':
            for option in conf.options(section):
                leader_dict[option] = conf.get(section, option)
        elif section == '006':
            for option in conf.options(section):
                tag_006_dict[option] = conf.get(section, option)
        elif section == '007':
            for option in conf.options(section):
                tag_007_dict[option] = conf.get(section, option)
        elif section == '008':
            for option in conf.options(section):
                tag_008_dict[option] = conf.get(section, option)
        elif section == '040':
            for option in conf.options(section):
                tag_040_dict[option] = conf.get(section, option)
        elif section == '264':
            for option in conf.options(section):
                tag_264_dict[option] = conf.get(section, option)

    record = Record(force_utf8=True)
    # set the leader
    record.leader = build_leader(leader_dict)
    # I *think* it's updating the 'Base Address of Data' position when
    # it is written to file, so I have kept characters 12-16 blank.
    # Field 005
    record.add_field(Field(tag='005', data=build_tag_005()))
    # Field 006
    record.add_field(Field(tag='006', data=build_tag_006(tag_006_dict, 
        tag_008_dict)))
    # Field 007
    record.add_field(Field(tag='007', data=build_tag_007(tag_007_dict)))
    # Field 008
    record.add_field(Field(tag='008', data=build_tag_008(tag_008_dict, 
        p, ns)))
    # Field 020
    if p.xpath('dc:identifier[@id="ISBN"]/text()', namespaces=ns):
        epub_isbn = p.xpath(
            'dc:identifier[@id="ISBN"]/text()', namespaces=ns)[0].strip()
        epub_field = Field(
            tag = '020',
            indicators = [' ', ' '],
            subfields = ['a', epub_isbn, 'q', 'epub']
                )
    elif p.xpath('dc:identifier[@pkg:scheme="ISBN"]/text()', namespaces=ns):
        epub_isbn = p.xpath(
                'dc:identifier[@pkg:scheme="ISBN"]/text()', namespaces=ns)[0].strip()

        epub_field = Field(
            tag = '020',
            indicators = [' ', ' '],
            subfields = ['a', epub_isbn, 'q', 'epub']
                )

    # Field 040
    # First, check if the indicators are empty and if they are,
    # turn them into single spaces.
    for value in ('indicator_1', 'indicator_2'):
        if tag_040_dict[value] == '':
            tag_040_dict[value] = ' '
    record.add_field(Field(
                tag = '040',
                indicators = [tag_040_dict['indicator_1'], 
                              tag_040_dict['indicator_2']],
                subfields = ['a', tag_040_dict['subfield_a'], 
                             'b', tag_040_dict['subfield_b'], 
                             'e', tag_040_dict['subfield_e'],
                             'c', tag_040_dict['subfield_c']]
    ))

    # Field 245
    if p.xpath('dc:title/text()',namespaces=ns):
        full_title = p.xpath('dc:title/text()',namespaces=ns)[0]
        if ":" in full_title:
            title = full_title[:full_title.index(':') ].strip()
            subtitle = full_title[full_title.index(':') + 1:].strip()
        else:
            title = full_title
            subtitle = None
    if p.xpath('dc:creator/text()', namespaces=ns)[0]:
        creator_statement = p.xpath('dc:creator/text()', namespaces=ns)[0]
    if title and subtitle and creator_statement:
        offset = 0
        if ' ' in title:
            title_words = title.split(' ')
            if title_words[0].lower() in NON_FILING_WORDS:
                offset = len(title_words[0]) + 1
        record.add_field(
            Field('245', ['0', offset], 
                ['a', title + " :", 
                 'b', subtitle + " /", 
                 'c', creator_statement]))
    elif title and creator_statement:
        offset = 0
        if ' ' in title:
            title_words = title.split(' ')
            if title_words[0].lower() in NON_FILING_WORDS:
                offset = len(title_words[0]) + 1
        record.add_field(
            Field('245', ['0', offset], 
                ['a', title + " /", 
                 'c', creator_statement]))

    # Field 264
    if p.xpath('dc:publisher/text()', namespaces=ns) \
    and p.xpath('dc:date/text()', namespaces=ns):
        record.add_field(Field('264', [' ', '1'], 
            ['a', tag_264_dict['subfield_a'] + ' :', 
             'b', p.xpath('dc:publisher/text()', namespaces=ns)[0] + ", ",
             'c', p.xpath('dc:date/text()', namespaces=ns)[0]]))
    if p.xpath('dc:rights/text()', namespaces=ns):
        copyright_statement = ""
        copyright_symbol = "©"
        rights_words_array = p.xpath('dc:rights/text()', 
            namespaces=ns)[0].split()
        for word in rights_words_array:
            if word in copyright_year_range:
                copyright_statement = copyright_symbol + word
        if len(copyright_statement) > 4:
            record.add_field(Field('264', [' ', '4'], 
                ['c', copyright_statement]))
    return record