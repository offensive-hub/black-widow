"""
*********************************************************************************
*                                                                               *
* html_parser.py -- HTML/URL parsing and Website crawling manager               *
*                                                                               *
********************** IMPORTANT BLACK-WIDOW LICENSE TERMS **********************
*                                                                               *
* This file is part of black-widow.                                             *
*                                                                               *
* black-widow is free software: you can redistribute it and/or modify           *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* black-widow is distributed in the hope that it will be useful,                *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with black-widow.  If not, see <http://www.gnu.org/licenses/>.          *
*                                                                               *
*********************************************************************************
"""

from abc import ABC
from html.parser import HTMLParser as PyHTMLParser
from urllib.parse import urlparse
from tidylib import tidy_document

from black_widow.app.managers.request import HttpRequest
from black_widow.app.services import Log
from black_widow.app.helpers.validators import is_url
from black_widow.app.helpers.util import is_listable


class HtmlParser(PyHTMLParser, ABC):
    """
    HtmlParser Manager
    """

    _relevant_tags = {
        'a': ['href'],  # { 'href': 'https://...' }
        'form': ['id', 'action', 'method'],
        # { 'action': 'https://...', 'method': 'GET', 'inputs': {'name': ['attr1', 'attr2']} }
        'input': [
            'id', 'name', 'type',
            'min', 'max',
            'required',
            'minlength',
            'maxlength',
            'pattern',
            'value'
        ],
        'textarea': [
            'id', 'name',
            'required',
            'minlength',
            'maxlength'
        ],
        'script': ['src', 'data', 'type'],  # { 'src': '/some/script.js', 'data': 'function() ...' }
        'link': ['href'],  # { 'href': '*.xml' }
        'html': [],
        'body': []
    }

    # Attributes witch contain URLs
    _url_attrs = ['href', 'src', 'action']

    # Not closed tags
    _not_closed_tags = ['input', 'link', 'meta', 'hr', 'img']

    def __init__(self, relevant: bool = False):
        super().__init__(self)
        self.tags = {}
        self.relevant = relevant
        self.queue_tag_ignored = []
        self.queue_tag = []
        self.queue_form = []
        self.url = None
        self.base_url = None
        self.url_scheme = ''

    @staticmethod
    def parse(url: str = None, html: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing ALL found tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :return: dictionary of tags, cookies
        """
        return HtmlParser._abstract_parse(url, html, False)

    @staticmethod
    def relevant_parse(url: str = None, html: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing only tags in HtmlParse._relevant_tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :return: dictionary of tags, cookies
        """
        return HtmlParser._abstract_parse(url, html, True)

    @staticmethod
    def form_parse(url: str = None, html: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing only tags in HtmlParse._relevant_tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :return: dictionary of form tags, cookies
        """
        parsed_html, cookies = HtmlParser.relevant_parse(url, html)
        return HtmlParser.find_forms(parsed_html, url), cookies

    @staticmethod
    def find_inputs(parsed: dict or list) -> dict:
        """
        Search inputs inside a parsed html (dict)
        :param parsed: A parsed html
        :return: A dictionary of input tags like {'input[name]': {'attr1': 'attr1_val' ...}}
        """
        inputs = {}
        if parsed is None:
            return inputs
        if type(parsed) == dict:
            tag = parsed.get('tag')
            if tag in ('input', 'textarea'):
                attrs = parsed.get('attrs')
                form_input = {'tag': tag}
                for key, value in attrs.items():
                    form_input[key] = value
                inputs[attrs.get('name')] = form_input
            inputs.update(HtmlParser.find_inputs(parsed.get('children')))
        elif type(parsed) == list:
            for value in parsed:
                inputs.update(HtmlParser.find_inputs(value))
        else:
            Log.error(str(parsed) + ' is not a valid parsed content!')
        return inputs

    @staticmethod
    def find_forms(parsed: dict or list, url=None) -> list:
        """
        Search forms inside parsed html (dict)
        :param parsed: A parsed html
        :param url: The parsed url (or None)
        :return: The list of found forms
        """
        forms = []
        if parsed is None:
            return forms
        if type(parsed) == dict:
            if 'form' == parsed.get('tag'):
                attrs = parsed.get('attrs')
                action = attrs.get('action')
                method = attrs.get('method')
                if action is None:
                    action = url
                if method is None:
                    method = HttpRequest.Type.POST
                form = {
                    'method': method,
                    'action': action,
                    'inputs': HtmlParser.find_inputs(parsed.get('children'))
                }
                forms.append(form)
            forms += HtmlParser.find_forms(parsed.get('children'), url)
        elif type(parsed) == list:
            for value in parsed:
                forms += HtmlParser.find_forms(value, url)
        else:
            Log.error(str(parsed) + ' is not a valid parsed content!')
        return forms

    @staticmethod
    def find_links(parsed: dict or list) -> set:
        """
        Search links inside a parsed html (dict)
        :param parsed: A parsed html
        :return: A set of found links
        """
        links = set()
        if parsed is None:
            return links
        if type(parsed) == dict:
            attrs = parsed.get('attrs')
            if attrs is not None:
                url = None
                if 'form' == parsed.get('tag'):
                    url = attrs.get('action')
                elif 'a' == parsed.get('tag'):
                    url = attrs.get('href')
                if url is not None:
                    links.add(url)
            links = links.union(HtmlParser.find_links(parsed.get('children')))
        elif type(parsed) == list:
            for value in parsed:
                links = links.union(HtmlParser.find_links(value))
        else:
            Log.error(str(parsed) + ' is not a valid parsed content!')
        return links

    @staticmethod
    def print_parsed(parsed: dict or list, depth: int = 0):
        """
        Print The result of methods @parse and @relevant_parse (so a parsed html)
        :param parsed: A parsed html
        :param depth: Current depth to build a pretty tree
        """
        space = ' ' * depth
        if type(parsed) == dict:
            print(space + '{')
            for key, value in parsed.items():
                if key == 'children':
                    HtmlParser.print_parsed(value, depth + 1)
                elif is_listable(value):
                    print((space + '  ') + str(key) + ':')
                    HtmlParser.print_parsed(value, depth + 2)
                    # print((space+'  ') + str(key) + ':')
                    # subspace = ' ' * (depth+1)
                    # for el in dict:
                    #  if (is_listable(el)):
                else:
                    print((space + '  ') + str(key) + ': ' + str(value))
            print(space + '}')
        elif type(parsed) == list:
            for value in parsed:
                HtmlParser.print_parsed(value, depth + 1)
        else:
            Log.error(str(parsed) + ' is not a valid parsed content!')

    @staticmethod
    def _abstract_parse(url: str, html: str, relevant: bool) -> (dict, str):
        """
        Make an HTML/URL parsing
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :param relevant: True if should be processed only the tags in HtmlParse._relevant_tags
        :return: dictionary of tags, cookies
        """
        parser = HtmlParser(relevant)
        return parser._parse(url, html)

    def handle_starttag(self, tag: str, attrs):
        """
        Start tag handler
        :param tag: The opened tag
        :param attrs: The attributes of opened tag like list[tuple{2}]
        """
        tag = str(tag).lower()
        if (not self.relevant) or tag in HtmlParser._relevant_tags.keys():
            tag_attrs = {}
            for attr in attrs:
                attr_key = str(attr[0]).lower()
                attr_value = str(attr[1])
                if (not self.relevant) or attr_key in HtmlParser._relevant_tags.get(tag):
                    if self.base_url is not None and attr_key in HtmlParser._url_attrs and (not is_url(attr_value)):
                        if attr_value[0:2] == '//':
                            attr_value = self.url_scheme + ':' + attr_value
                        else:
                            if attr_value[0:1] != '/':
                                attr_value = '/' + attr_value
                            attr_value = self.base_url + attr_value
                    tag_attrs[attr_key] = attr_value
            cur_tag = {'tag': tag, 'attrs': tag_attrs}
            self.queue_tag.append(cur_tag)
            if tag in HtmlParser._not_closed_tags:
                self.handle_endtag(tag)
        else:
            self.queue_tag_ignored.append(tag)

    def handle_endtag(self, tag: str):
        """
        Closing tag handler
        :param tag: The closing tag
        """
        tag = str(tag).lower()
        if len(self.queue_tag_ignored) > 0 and tag == self.queue_tag_ignored[-1]:
            self.queue_tag_ignored.pop()
            return
        if len(self.queue_tag) == 0:
            return
        cur_tag = self.queue_tag.pop()
        self._nest_tag(cur_tag)

    def handle_data(self, data: str):
        """
        Tag content tag handler
        :param data: The last opened tag content
        """
        if len(self.queue_tag) == 0:
            return
        cur_tag = self.queue_tag[-1]
        if (not self.relevant) or 'data' in HtmlParser._relevant_tags.get(cur_tag.get('tag')):
            cur_tag['data'] = data
            self.queue_tag[-1] = cur_tag

    def _parse(self, url: str = None, html: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing ALL found tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :return: dictionary of tags, cookies
        """
        self.url = None
        self.base_url = None
        cookies = ''
        if url is not None:
            self.url = url
            url_parsed = urlparse(url)
            self.url_scheme = str(url_parsed.scheme)
            self.base_url = self.url_scheme + '://' + str(url_parsed.netloc)
            r = HttpRequest.request(url)
            if r is None:
                return None
            try:
                html = r.json()
                Log.warning('Trying to parse a json with HTML parser!')
            except ValueError:
                html = r.text
            if r.headers is not None:
                for k in r.headers.keys():
                    if k == 'Set-Cookie' or k == 'set-cookie' or k == 'Set-cookie':
                        cookies = r.headers.get('Set-Cookie')
                        break
        sorted_html, errors = tidy_document(html)   # Sort html (and fix errors)
        self.feed(sorted_html)
        return self.tags, cookies

    def _nest_tag(self, tag_dict: dict):
        """
        Insert the input tag inside the last one of queue
        :param tag_dict: A parsed-tag dictionary
        :return: void
        """
        queue_tag_len = len(self.queue_tag)
        if queue_tag_len == 0:
            parent = self.tags
        else:
            parent = self.queue_tag[-1]
        parent_children = parent.get('children')
        if parent_children is None:
            parent_children = []
        parent_children.append(tag_dict)
        parent['children'] = parent_children
        if queue_tag_len == 0:
            self.tags = parent
        else:
            self.queue_tag[-1] = parent
