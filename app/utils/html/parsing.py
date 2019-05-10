import json
from html.parser import HTMLParser
from urllib.parse import urlparse
from app.utils.requests import request, Type as RequestType
from app.utils.helpers.validators import is_url

# Black Widow HTML Parser
class Parser(HTMLParser):
    # Tags rilevanti
    relevant_tags = {
        'a': ['href'],                      # { 'href': 'https://...' }
        'form': ['action', 'method'],       # { 'action': 'https://...', 'method': 'GET', 'inputs': {'name': ['attr1', 'attr2']} }
        'input': [
            'id','name','type',
            'min','max',
            'required',
            'minlength',
            'maxlength',
            'pattern',
            'value'
        ],
        'textarea': [
            'id','name',
            'required',
            'minlength',
            'maxlength'
        ],
        'script': ['src', 'data', 'type'],  # { 'src': '/some/script.js', 'data': 'function() ...' }
        'link': ['href'],                   # { 'href': '*.xml' }
        'html': [],
        'body': []
    }
    # Attributi contenenti url
    url_attrs = ['href', 'src', 'action']
    # Tag non chiuse (ignorare handle_endtag)
    not_closed_tags = ['input', 'link', 'meta']

    def __init__(self, relevant=False):
        HTMLParser.__init__(self)
        self.tags = {}
        self.relevant = relevant
        self.queue_tag_ignored = []
        self.queue_tag = []
        self.queue_form = []

    # inserisce la tag passata per argomento, dentro l'ultima della coda
    def __nest_tag__(self, tag_dict):
        tag = tag_dict.get('tag')
        if (len(self.queue_tag) == 0): parent = self.tags
        else: parent = self.queue_tag[-1]
        parent_children = parent.get('children')
        if (parent_children == None): parent_children = []
        parent_children.append(tag_dict)
        parent['children'] = parent_children
        if (len(self.queue_tag) == 0): self.tags = parent
        else: self.queue_tag[-1] = parent

    def handle_starttag(self, tag, attrs):
        tag = str(tag).lower()
        if ((not self.relevant) or tag in Parser.relevant_tags.keys()):
            tag_attrs={}
            for attr in attrs:
                attr_key = str(attr[0]).lower()
                attr_value = str(attr[1])
                if ((not self.relevant) or attr_key in Parser.relevant_tags.get(tag)):
                    if (self.base_url != None and attr_key in Parser.url_attrs and (not is_url(attr_value))):
                        if (attr_value[0:2] == '//'):
                            attr_value = self.url_scheme + ':' + attr_value
                        else:
                            if (attr_value[0:1] != '/'): attr_value = '/' + attr_value
                            attr_value = self.base_url + attr_value
                    tag_attrs[attr_key] = attr_value
            cur_tag = {'tag': tag, 'attrs': tag_attrs}
            self.queue_tag.append(cur_tag)
            if (tag in Parser.not_closed_tags): self.handle_endtag(tag)
        else: self.queue_tag_ignored.append(tag)

    def handle_endtag(self, tag):
        tag = str(tag).lower()
        if (len(self.queue_tag_ignored) > 0 and tag == self.queue_tag_ignored[-1]):
            self.queue_tag_ignored.pop()
            return
        if (len(self.queue_tag) == 0): return
        cur_tag = self.queue_tag.pop()
        if (tag == cur_tag.get('tag')): self.__nest_tag__(cur_tag)

    def handle_data(self, data):
        if (len(self.queue_tag) == 0): return
        cur_tag = self.queue_tag[-1]
        if ((not self.relevant) or 'data' in Parser.relevant_tags.get(cur_tag.get('tag'))):
            cur_tag['data'] = data
            self.queue_tag[-1] = cur_tag

    # Fa il parsing della risposta dell'url passato per argomento
    # @param url L'url del quale fare il parsing della risposta
    # @param html L'html di cui ottenere il parsing
    def parse(self, url=None, html=None):
        if (url != None):
            self.url = url
            url_parsed = urlparse(url)
            self.url_scheme = str(url_parsed.scheme)
            self.base_url = self.url_scheme + '://' + str(url_parsed.netloc)
            r = request(url, RequestType.GET)
            if (r == None): return None
            try:
                html = r.json()
                Log.warning('Trying to parse a json with HTML parser!')
            except json.decoder.JSONDecodeError:
                html = r.text
        else:
            self.url = None
            self.base_url = None
        self.feed(html)
        return self.tags

def __parse__(url, html, relevant):
    parser = Parser(relevant)
    return parser.parse(url)

# Esegue un parsing di tutte le tag
def parse(url=None, html=None):
    return __parse__(url, html, False)

# Esegue un parsing solo delle tag rilevanti
def relevant_parse(url=None, html=None):
    return __parse__(url, html, True)

def find_inputs(parsed):
    inputs = {}
    if (parsed == None): return inputs
    if (type(parsed) == dict):
        tag = parsed.get('tag')
        if (tag in ('input', 'textarea')):
            attrs = parsed.get('attrs')
            input = {'tag': tag}
            for key,value in attrs.items(): input[key] = value
            inputs[attrs.get('name')] = input
        inputs.update(find_inputs(parsed.get('children')))
    elif (type(parsed) == list):
        for value in parsed: inputs.update(find_inputs(value))
    else: Log.error(str(parsed)+' is not a valid parsed content!')
    return inputs

def find_forms(parsed):
    forms = []
    if (parsed == None): return forms
    if (type(parsed) == dict):
        if ('form' == parsed.get('tag')):
            attrs = parsed.get('attrs')
            form = {
                'method': attrs.get('method'),
                'action': attrs.get('action'),
                'inputs': find_inputs(parsed.get('children'))
            }
            forms.append(form)
        forms += find_forms(parsed.get('children'))
        return forms
    elif (type(parsed) == list):
        for value in parsed: forms += find_forms(value)
    else: Log.error(str(parsed)+' is not a valid parsed content!')
    return forms



# Printa il risultato delle funzioni @parse e @relevant_parse
def print_parsed(parsed, depth=0):
    space = ' ' * depth
    if (type(parsed) == dict):
        print(space + '{')
        for key, value in parsed.items():
            if (key == 'children'): print_parsed(value, depth+1)
            else: print((space*2) + str(key) + ': ' + str(value))
        print(space + '}')
    elif (type(parsed) == list):
        for value in parsed: print_parsed(value, depth+1)
    else:
        Log.error(str(parsed)+' is not a valid parsed content!')
