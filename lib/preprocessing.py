import re
import html

whitespace_pattern = re.compile(r'\s+')

def remove_tags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def unescape_html(raw_html):
    return html.unescape(raw_html)

def remove_whitespace(text):
    return whitespace_pattern.sub(' ', text)