import json
from html.parser import HTMLParser
from app.utils.requests import request, Type as RequestType

# Black Widow HTML Parser
class Parser(HTMLParser):
    relevant_tags = {
        'a': ['href'],                 # { 'href': 'https://...' }
        'form': ['action', 'method'],  # { 'action': 'https://...', 'method': 'GET', 'inputs': {'name': ['attr1', 'attr2']} }
        'input': [
            'name','type',
            'min', 'max',
            'required',
            'minlength',
            'maxlength',
            'pattern'
        ],
        'textarea': [
            'name',
            'required',
            'minlength',
            'maxlength'
        ],
        'script': ['src', 'data'],     # { 'src': '/some/script.js', 'data': 'function() ...' }
        'link': ['href']               # { 'href': '*.xml' }
    }
    not_closed_tags = ['input', 'link']

    def __init__(self, relevant=False):
        HTMLParser.__init__(self)
        self.tags = {}
        self.relevant = relevant
        self.queue_tag_ignored = []
        self.queue_tag = []
        self.queue_form = []

    def handle_starttag(self, tag, attrs):
        tag = str(tag).lower()
        if ((not self.relevant) or tag in Parser.relevant_tags.keys()):
            tag_attrs={}
            for dirty_attr in attrs:
                attr_key = str(dirty_attr[0]).lower()
                attr_value = str(dirty_attr[1]).lower()
                if ((not self.relevant) or attr_key in Parser.relevant_tags[tag]):
                    tag_attrs[attr_key] = attr_value
            cur_tag = {'tag': tag, 'attrs': tag_attrs}
            if (tag in Parser.not_closed_tags):
                if (self.tags.get(tag) == None): self.tags[tag] = []
                self.tags[tag].append(cur_tag)
            else: self.queue_tag.append(cur_tag)
        else:
            self.queue_tag_ignored.append(tag)

    def handle_endtag(self, tag):
        tag = str(tag).lower()
        if (len(self.queue_tag_ignored) > 0 and tag == self.queue_tag_ignored[-1]):
            self.queue_tag_ignored.pop()
            return
        if (len(self.queue_tag) == 0): return
        cur_tag = self.queue_tag.pop()
        if (cur_tag != None and tag == cur_tag.get('tag')):
            if (self.tags.get(tag) == None): self.tags[tag] = []
            self.tags[tag].append(cur_tag)

    def handle_data(self, data):
        if (len(self.queue_tag) == 0): return
        cur_tag = self.queue_tag[-1]
        if ((not self.relevant) or 'data' in Parser.relevant_tags.get(cur_tag.get('tag'))):
            cur_tag['data'] = data
            self.queue_tag[-1] = cur_tag

    # Fa il parsing della risposta dell'url passato per argomento
    # @param url L'url del quale fare il parsing della risposta
    def parse(self, url):
        r = request(url, RequestType.GET)
        if (r == None): return None
        try:
            r_result = r.json()
            Log.warning('Trying to parse a json with HTML parser!')
        except json.decoder.JSONDecodeError:
            r_result = r.text
        self.feed(r_result)
        return self.tags

def parse(url):
    parser = Parser()
    return parser.parse(url)

def relevant_parse(url):
    parser = Parser(True)
    return parser.parse(url)
