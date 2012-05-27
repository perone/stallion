"""
.. module:: metadata
   :platform: Unix, Windows
   :synopsis: Pacakge metadata parsing.

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`metadata` -- package metadata parser
==================================================================
"""

import string
from email.parser import Parser
import pkg_resources

# Tuple metadata format
# (Field Name, lowered field name, Optional)

# Based on the PEP-0241
HEADER_META_1_0 = (
    'metadata-version',
    'name',
    'version',
    'platform',
    'supported-platform',
    'summary',
    'description',
    'keywords',
    'home-page',
    'author',
    'author-email',
    'license',
    # Not part of PEP, but PEP-0314 (everyone uses anyway in 1.0)
    'classifier'
)

# Based on the PEP-0314
HEADER_META_1_1 = HEADER_META_1_0 + (
    'download-url',
    'requires',
    'provides',
    'obsoletes',
)

# Based on the PEP-0345
HEADER_META_1_2 = HEADER_META_1_1 + (
    'maintainer',
    'maintainer-email',
    'requires-python',
    'requires-external',
    'requires-dist',
    'provides-dist',
    'obsoletes-dist',
    'project-url',
)

HEADER_META = {
    '1.0': HEADER_META_1_0,
    '1.1': HEADER_META_1_1,
    '1.2': HEADER_META_1_2,
}

METADATA_NAME = 'PKG-INFO'


def parse_metadata(metadata):
    """ Parse the package PKG-INFO metadata. Currently supports versions 1.0 (PEP-0241),
    1.1 (PEP-0314), 1.2 (PEP-0345).

    :param metadata: the raw PKG-INFO metadata text
    :type metadata: string
    :rtype: tuple
    :return: (parsed_metadata, key_known), the parsed_metadata is the rfc822.Message
             object and the key_known is the fields found in the metadata info which
             is part of the metadata version specification
    """
    parsed_metadata = Parser().parsestr(metadata)
    metadata_spec = set(HEADER_META[parsed_metadata['metadata-version']])
    key_exist = set([s.lower() for s in parsed_metadata.keys()])
    return (parsed_metadata, key_exist.intersection(metadata_spec))


def clean_lead_ws_description(metadata, field_name):
    """ Sometimes the metadata fields are a mess, this function is intended to remove the leading
    extra space some authors add in front of the 'description' field and to handle some other
    field cases.

    :param metadata: the metadata text
    :param field_name: the name of the field, like 'description'
    :rtype: string
    :return: the processed metadata
    """
    def calc_leading(line):
        return len(line) - len(line.lstrip())

    def most_common(lst):
        return max(set(lst), key=lst.count)

    if field_name.lower() == 'description':
        leading_ws_count = [calc_leading(line) for line in metadata.splitlines()]
        most_common_ws_count = most_common(leading_ws_count)

        strip_split = metadata.strip().splitlines()
        return '\n'.join([line[most_common_ws_count:] if line.startswith(' ' * most_common_ws_count) else line
                          for line in strip_split])
    else:
        return ' '.join([line.strip() for line in metadata.splitlines()])


def field_process(field_name, field_value):
    """ Processes a field, it changes the 'UNKNOWN' values for None, clear leading whitespaces, etc.

    :param field_name: the field name
    :param field_value: the value of the field
    :rtype: string or list
    :return: field value processed
    """

    if field_name == 'classifier':
        root = {}
        for line in field_value:
            d = root
            path_split = tuple([s.strip() for s in line.split('::')])
            for level in path_split:
                if level in d:
                    d = d[level]
                else:
                    b = {}
                    d[level] = b
                    d = b

        return root

    if isinstance(field_value, list):
        return field_value

    f_value = clean_lead_ws_description(field_value, field_name)

    if hasattr(f_value, 'decode'):
        f_value = f_value.decode('utf-8')

    if f_value == 'UNKNOWN':
        return None

    if field_name == 'keywords':
        f_value = field_value.split(',' if ',' in field_value else ' ')

    return f_value


def metadata_to_dict(parsed_metadata, key_known):
    """ This is the main function used to process the parsed metadata into a structured
    and pre-processed data dictionary.

    :param parsed_metadata: the return of the function :func:`stallion.metadata.parse_metadata`.
    :rtype: dictionary
    :returns: the processed metadata dictionary
    """

    mdict = {}

    for field in set(parsed_metadata.keys()):
        all_values = parsed_metadata.get_all(field)
        if len(all_values) == 1:
            all_values = all_values[0]

        fl_name = field.lower()
        fl_processed = field_process(fl_name, all_values)
        if fl_processed:
            mdict[fl_name] = fl_processed

    return mdict
