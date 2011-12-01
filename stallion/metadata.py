"""
.. module:: metadata
   :platform: Unix, Windows
   :synopsis: Pacakge metadata parsing.

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`metadata` -- package metadata parser
==================================================================
"""

#import rfc822
from email.parser import Parser
import pkg_resources

# Tuple metadata format
# (Field Name, lowered field name, Optional)

# Based on the PEP-0241
HEADER_META_1_0 = (
    ('Metadata-Version', 'metadata-version', False),
    ('Name', 'name', False),
    ('Version', 'version', False),
    ('Platform', 'platform', True),
    ('Supported-Platform', 'supported-platform', True),
    ('Summary', 'summary', False),
    ('Description', 'description', False),
    ('Keywords', 'keywords', False),
    ('Home-Page', 'home-page', False),
    ('Author', 'author', False),
    ('Author-email', 'author-email', False),
    ('License', 'license', False),
)

# Based on the PEP-0314
HEADER_META_1_1 = HEADER_META_1_0 + ( 
    ('Classifier', 'classifiers', True),
    ('Download-URL', 'download-url', False),
    ('Requires', 'requires', True),
    ('Provides', 'provides', True),
    ('Obsoletes', 'obsoletes', True),
)

# Based on the PEP-0345
HEADER_META_1_2 = HEADER_META_1_1 + (
    ('Maintainer', 'maintainer', False),
    ('Maintainer-email', 'maintainer-email', False),
    ('Requires-Python', 'requires-python', False),
    ('Requires-External', 'requires-external', True),
    ('Requires-Dist', 'requires-dist', True),
    ('Provides-Dist', 'provides-dist', True),
    ('Obsoletes-Dist', 'obsoletes-dist', True),
    ('Project-URL', 'project-url', True),
)

HEADER_META = {
    '1.0': HEADER_META_1_0,
    '1.1': HEADER_META_1_1,
    '1.2': HEADER_META_1_2,
}

METADATA_NAME = "PKG-INFO"

def parse_metadata(metadata):
    """ Parse the package PKG-INFO metadata. Currently supports versions 1.0 (PEP-0241),
    1.1 (PEP-0314), 1.2 (PEP-0345).
    
    :param metadata: the raw PKG-INFO metadata text
    :type metadata: string
    :rtype: tuple 
    :return: (parsed_metadata, key_exist, key_known), the parsed_metadata is the rfc822.Message
             object, the key_exist are the fields which were found in the package, the key_known are
             the valid fields according to its metadata version.
    """
    parsed_metadata = Parser().parsestr(metadata)
    metadata_spec = HEADER_META[parsed_metadata["metadata-version"]]
    key_exist = set(parsed_metadata.keys())
    key_known = set([key_name for field_name, key_name, optional in metadata_spec])
    return (parsed_metadata, key_exist, key_known)

def clean_leading_ws(txt, key_name):
    def calc_leading(line):
        return len(line) - len(line.lstrip())

    def most_common(lst):
        return max(set(lst), key=lst.count)

    if key_name.lower() == 'description':
        leading_ws_count = [calc_leading(line) for line in txt.splitlines()]
        most_common_ws_count = most_common(leading_ws_count)
        
        strip_split = txt.strip().splitlines()
        return '\n'.join([line[most_common_ws_count:] if line.startswith(' ' * most_common_ws_count) else line
                          for line in strip_split])
    else:
        return ' '.join([line.strip() for line in txt.splitlines()])

def run_test():
    pkg = pkg_resources.get_distribution("jinja2")
    parsed, key_exist, key_known = parse_metadata(pkg.get_metadata(METADATA_NAME))
    print parsed
    print key_exist
    print key_known

if __name__ == "__main__":
    run_test()




