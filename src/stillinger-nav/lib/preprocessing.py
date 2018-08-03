import re
import sys

def is_version_3():
    return sys.version_info == (3,)

whitespace_pattern = re.compile(r'\s+')

def remove_tags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def unescape_html(raw_html):
    if is_version_3():
        import html
        return html.unescape(raw_html)
    else:
        import HTMLParser
        return HTMLParser.HTMLParser().unescape(raw_html)

def remove_whitespace(text):
    return whitespace_pattern.sub(' ', text)