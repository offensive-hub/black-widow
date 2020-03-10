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
from black_widow.app.services import Log, JsonSerializer
from black_widow.app.helpers.validators import is_url
from black_widow.app.helpers.util import is_listable


class HtmlParser(PyHTMLParser, ABC):
    """
    HtmlParser Manager
    """

    TYPE_ALL = 'all_parse'
    TYPE_RELEVANT = 'relevant_parse'
    TYPE_FORM = 'form_parse'
    TYPE_META = 'meta_parse'

    _input_tags = {
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
            'id', 'name', 'data',
            'required',
            'minlength',
            'maxlength'
        ],
        'select': [
            'id', 'name', 'required'
        ],
        'option': [
            'id', 'value', 'selected'
        ],
        'button': [
            'id', 'name', 'type', 'form', 'value'
        ]
    }

    _xmp_tags = {
        'x:xmpmeta': ['xmlns:x', 'x:xmptk'],
        'rdf:rdf': ['xmlns:rdf'],
        'rdf:description': [
            'data',
            'rdf:about',
            'xmlns:dc',
            'xmlns:xmp',
            'xmlns:xmpRights',
            'xmp:CreatorTool',
            'xmpRights:Marked',
            'xmpRights:Marked'
        ],
        'rdf:seq': ['data'],
        'rdf:li': ['data'],
        'rdf:alt': ['data'],
        'dc:contributor': ['data'],
        'dc:coverage': ['data'],
        'dc:creator': ['data'],
        'dc:date': ['data'],
        'dc:description': ['data'],
        'dc:format': ['data'],
        'dc:identifier': ['data'],
        'dc:language': ['data'],
        'dc:publisher': ['data'],
        'dc:relation': ['data'],
        'dc:rights': ['data'],
        'dc:source': ['data'],
        'dc:subject': ['data'],
        'dc:title': ['data'],
        'dc:type': ['data']
    }

    _meta_tags = {
        'meta': ['name', 'itemprop', 'property', 'content', 'charset']
    }
    _meta_tags.update(_xmp_tags)

    _tag_names = ('name', 'itemprop', 'property', 'id')
    _tag_key_names = ('content', 'charset')

    _relevant_tags = {
        'a': ['href'],
        'img': ['src'],
        'form': ['id', 'action', 'method', 'name'],
        'script': ['src', 'data', 'type'],  # { 'src': '/some/script.js', 'data': 'function() ...' }
        'link': ['href'],  # { 'href': '*.xml' }
        'html': [],
        'body': []
    }
    _relevant_tags.update(_input_tags)
    _relevant_tags.update(_meta_tags)

    # Attributes witch contain URLs
    _url_attrs = ['href', 'src', 'action']

    # Not closed tags
    _not_closed_tags = ['input', 'link', 'meta', 'hr', 'img', 'br']

    def __init__(self, relevant: bool = False):
        super().__init__()
        self.tags = {}
        self.relevant = relevant
        self.queue_tag_ignored = []
        self.queue_tag = []
        self.queue_form = []
        self.url = None
        self.base_url = None
        self.url_scheme = ''

    @staticmethod
    def crawl(url: str, parsing_type: str, callback, depth: int = 0, cookies: str = None):
        """
        :param url: The url to crawl/parse
        :param parsing_type: HtmlParse.TYPE_ALL | HtmlParse.TYPE_RELEVANT | HtmlParse.TYPE_FORM | HtmlParse.TYPE_META
        :param callback: The callback method to call foreach visited page
        :param depth: The max crawling depth (0 to execute a normal page parsing, < 0 for no limit)
        :param cookies: The cookies to use on parsing
        """
        if not is_url(url):
            raise ValueError('url must be a valid url')
        if parsing_type not in HtmlParser.types():
            raise ValueError('parsing_type must be one of ' + str(HtmlParser.types()))
        if not callable(callback):
            raise ValueError('callback is not callable')
        if type(depth) is not int:
            raise ValueError('dept must be an integer')
        if cookies is not None and type(cookies) is not str:
            raise ValueError('cookies must be a string')

        base_url = urlparse(url).netloc
        base_urls = (base_url, )
        if base_url[0:4] != 'www.':
            base_urls += ('www.' + str(base_url),)
        parsed_urls = set()
        parsed_hashes = set()

        def _crawl(href: str, curr_depth: int = 0):
            if href in parsed_urls or \
                    urlparse(href).netloc not in base_urls or \
                    (0 <= depth and (depth < curr_depth)):
                return

            # Visit the current href
            if parsing_type == HtmlParser.TYPE_ALL:
                parsed, _ = HtmlParser.all_parse(href, cookies=cookies)
            else:
                parsed, _ = HtmlParser.relevant_parse(href, cookies=cookies)

            parsed_hash = hash(JsonSerializer.dump_json(parsed))
            if parsed_hash in parsed_hashes:
                return

            parsed_hashes.add(parsed_hash)
            parsed_urls.add(href)

            if parsing_type == HtmlParser.TYPE_FORM:
                # Find forms in page
                parsed_page = HtmlParser.find_forms(parsed, href)
            elif parsing_type == HtmlParser.TYPE_META:
                # Find metadata in page
                parsed_page = HtmlParser.find_meta(parsed)
            else:
                parsed_page = parsed

            if parsed_page.get('tag') is not None:
                parsed_page = {
                    0: parsed_page
                }

            parsed_page['url'] = href
            callback(parsed_page)

            # Find adjacent links
            links = HtmlParser.find_links(parsed)
            for link in links:
                _crawl(link, curr_depth + 1)

        _crawl(url)
        Log.success(url + ' crawling done!')

    @staticmethod
    def all_parse(url: str = None, html: str = None, cookies: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing ALL found tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :param cookies: The cookies to use on parsing
        :return: dictionary of tags, cookies
        """
        return HtmlParser.__abstract_parse(url, html, False, cookies)

    @staticmethod
    def relevant_parse(url: str = None, html: str = None, cookies: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing only tags in HtmlParse._relevant_tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :param cookies: The cookies to use on parsing
        :return: dictionary of tags, cookies
        """
        return HtmlParser.__abstract_parse(url, html, True, cookies)

    @staticmethod
    def form_parse(url: str = None, html: str = None, cookies: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing only tags in HtmlParse._relevant_tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :param cookies: The cookies to use on parsing
        :return: dictionary of form tags, cookies
        """
        parsed_html, cookies = HtmlParser.relevant_parse(url, html, cookies)
        return HtmlParser.find_forms(parsed_html, url), cookies

    @staticmethod
    def find_meta(parsed: dict or list) -> dict:
        """
        Search metadata inside a parsed html (dict)
        :param parsed: A parsed html
        :return: A dictionary of metadata tags like {'meta[name]': {'attr1': 'attr1_val' ...}}
        """
        return HtmlParser.__find_tags(parsed, HtmlParser._meta_tags)

    @staticmethod
    def find_forms(parsed: dict or list, url=None) -> dict:
        """
        Search forms inside parsed html (dict)
        :param parsed: A parsed html
        :param url: The parsed url (or None)
        :return: The list of found forms
        """
        form = dict()
        if parsed is None:
            return form
        if type(parsed) == dict:
            parsed_children = parsed.get('children')
            if 'form' == parsed.get('tag'):
                attrs = parsed.get('attrs')
                action = attrs.get('action')
                method = attrs.get('method')
                name = attrs.get('name')
                if action is None:
                    action = url
                if method is None:
                    method = HttpRequest.Type.POST
                attrs = {
                    'method': method,
                    'action': action,
                    'name': name
                }
                if name is None:
                    name = action
                form = {
                    'tag': 'form',
                    'attrs': attrs,
                    'name': name,
                    'children': HtmlParser.__find_inputs(parsed_children)
                }
            children = HtmlParser.find_forms(parsed_children, url)
            if children is not None and len(children) > 0:
                if len(form) > 0:
                    form['children'] = children
                else:
                    if len(children) == 1 and children.get('tag') is None:
                        form = children.get(0)
                    else:
                        form = children
        elif type(parsed) is list:
            children = dict()
            index = 0
            for value in parsed:
                child = HtmlParser.find_forms(value, url)
                if len(child) > 0:
                    children[index] = child
                    index += 1
            if len(children) == 1 and children.get(0).get('tag') is None:
                form = children.get(0)
            else:
                form = children
        else:
            Log.error(str(parsed) + ' is not a valid parsed content!')
        return form

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
        if type(parsed) is dict:
            attrs = parsed.get('attrs')
            if attrs is not None:
                url = None
                if 'form' == parsed.get('tag'):
                    url = attrs.get('action')
                elif 'a' == parsed.get('tag'):
                    url = attrs.get('href')
                    if url is not None and 'email-protection' in url:
                        # Skip email protections
                        url = None
                elif 'img' == parsed.get('tag'):
                    url = attrs.get('src')
                if url is not None:
                    links.add(url)
            links = links.union(HtmlParser.find_links(parsed.get('children')))
        elif type(parsed) is list:
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
                else:
                    print((space + '  ') + str(key) + ': ' + str(value))
            print(space + '}')
        elif type(parsed) == list:
            for value in parsed:
                HtmlParser.print_parsed(value, depth + 1)
        else:
            Log.error(str(parsed) + ' is not a valid parsed content!')

    @staticmethod
    def types() -> tuple:
        return (
            HtmlParser.TYPE_ALL,
            HtmlParser.TYPE_RELEVANT,
            HtmlParser.TYPE_FORM,
            HtmlParser.TYPE_META
        )

    @staticmethod
    def type_descriptions() -> dict:
        return {
            HtmlParser.TYPE_ALL: 'Parse all tags',
            HtmlParser.TYPE_RELEVANT: 'Parse anchor, script, links, forms, images',
            HtmlParser.TYPE_FORM: 'Parse forms',
            HtmlParser.TYPE_META: 'Parse metadata'
        }

    @staticmethod
    def __abstract_parse(url: str, html: str, relevant: bool, cookies: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :param relevant: True if should be processed only the tags in HtmlParse._relevant_tags
        :param cookies: The cookies to use on parsing
        :return: dictionary of tags, cookies
        """
        parser = HtmlParser(relevant)
        return parser.__parse(url, html, cookies)

    @staticmethod
    def __find_tags(parsed: dict or list, tags: dict) -> dict:
        """
        Search a certain kinds of tag inside a parsed html (dict)
        :param parsed: A parsed html
        :tags parsed: The tags to find
        :return: A dictionary of tags like {'tag[name]': {'attr1': 'attr1_val' ...}}
        """
        found_tag = {}
        if parsed is None:
            return found_tag
        if type(parsed) is dict:
            tag: str = parsed.get('tag')
            if tag is not None:
                tag = tag.lower()
            if tag in tags:
                attrs = parsed.get('attrs')
                # Tag
                found_tag = {'tag': tag}
                # Tag attrs
                found_tag_attrs = dict()
                for key, value in attrs.items():
                    found_tag_attrs[key] = value.strip()
                found_tag['attrs'] = found_tag_attrs
                # Tag data
                found_tag['data'] = parsed.get('data')
                # Tag name
                name = None
                for tag_name in HtmlParser._tag_names:
                    name = attrs.get(tag_name)
                    if name is not None:
                        break
                if name is None:
                    for tag_key in HtmlParser._tag_key_names:
                        name = attrs.get(tag_key)
                        if name is not None:
                            name = tag_key
                            break
                if name is None:
                    name = tag
                found_tag['name'] = name
            # Tag children
            children = HtmlParser.__find_tags(parsed.get('children'), tags)
            if children is not None and len(children) > 0:
                if len(found_tag) > 0:
                    found_tag['children'] = children
                else:
                    if len(children) == 1 and children.get(0).get('name') is None:
                        found_tag = children.get(0)
                    else:
                        found_tag = children
        elif type(parsed) is list:
            children = dict()
            index = 0
            for value in parsed:
                child = HtmlParser.__find_tags(value, tags)
                if len(child) > 0:
                    children[index] = child
                    index += 1
            if len(children) == 1 and children.get(0).get('name') is None:
                found_tag = children.get(0)
            else:
                found_tag = children
        else:
            Log.error(str(parsed) + ' is not a valid parsed content!')
        return found_tag

    @staticmethod
    def __find_inputs(parsed: dict or list) -> dict:
        """
        Search inputs inside a parsed html (dict)
        :param parsed: A parsed html
        :return: A dictionary of input tags like {'input[name]': {'attr1': 'attr1_val' ...}}
        """
        return HtmlParser.__find_tags(parsed, HtmlParser._input_tags)

    def handle_starttag(self, tag: str, attrs):
        """
        Start tag handler
        :param tag: The opened tag
        :param attrs: The attributes of opened tag like list[tuple{2}]
        """
        tag = str(tag).lower()
        if self.relevant and tag not in HtmlParser._relevant_tags.keys():
            self.queue_tag_ignored.append(tag)
            if tag in HtmlParser._not_closed_tags:
                self.handle_endtag(tag)
            return
        tag_attrs = {}
        for attr in attrs:
            attr_key = str(attr[0]).lower()
            attr_value = str(attr[1])
            if self.relevant and attr_key not in HtmlParser._relevant_tags.get(tag):
                continue
            if self.base_url is not None and attr_key in HtmlParser._url_attrs and (not is_url(attr_value)):
                if len(attr_value) == 0:
                    continue
                if attr_value[0] == '#':
                    continue
                if attr_value[0:2] == '//':
                    attr_value = self.url_scheme + ':' + attr_value
                else:
                    if attr_value[0] != '/' and self.base_url[len(self.base_url) - 1] != '/':
                        attr_value = '/' + attr_value
                    elif attr_value[0] == '/' and self.base_url[len(self.base_url) - 1] == '/':
                        attr_value = attr_value[1:]
                    attr_value = self.base_url + attr_value
            if 'email-protection' in attr_value:
                attr_value = 'email-protection'
            tag_attrs[attr_key] = attr_value
        cur_tag = {'tag': tag, 'attrs': tag_attrs}
        self.queue_tag.append(cur_tag)
        if tag in HtmlParser._not_closed_tags:
            self.handle_endtag(tag)

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
        self.__nest_tag(cur_tag)

    def handle_data(self, data: str):
        """
        Tag content tag handler
        :param data: The last opened tag content
        """
        if len(self.queue_tag) == 0:
            return
        cur_tag = self.queue_tag[-1]
        if (not self.relevant) or 'data' in HtmlParser._relevant_tags.get(cur_tag.get('tag')):
            cur_tag['data'] = data.strip()
            self.queue_tag[-1] = cur_tag

    def __parse(self, url: str = None, html: str = None, cookies: str = None) -> (dict, str):
        """
        Make an HTML/URL parsing by processing ALL found tags
        :param url: The url to parse (or None)
        :param html: The html page to parse as string (or None)
        :param cookies: The cookies to use on parsing
        :return: dictionary of tags, cookies
        """
        self.url = None
        self.base_url = None
        is_image = False
        if url is not None:
            self.url = url
            url_parsed = urlparse(url)
            self.url_scheme = str(url_parsed.scheme)
            self.base_url = self.url_scheme + '://' + str(url_parsed.netloc)
            r = HttpRequest.request(url, cookies=cookies)
            if r is None:
                return None
            try:
                html = r.json()
                Log.warning('Trying to parse a json with HTML parser!')
            except ValueError:
                html = r.text
            if r.headers is not None:
                for k, v in r.headers.items():
                    if k.lower() == 'set-cookie':
                        cookies = v
            if HttpRequest.is_image(r):
                is_image = True
                xmp_start = html.find('<x:xmpmeta')
                xmp_end = html.find('</x:xmpmeta')
                xmp_str = html[xmp_start:xmp_end+12]
                html = xmp_str
        if is_image:
            sorted_html = html
        else:
            sorted_html, errors = tidy_document(html)   # Sort html (and fix errors)
        self.feed(sorted_html)
        if cookies is None:
            cookies = ''
        return self.tags, cookies

    def __nest_tag(self, tag_dict: dict):
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
