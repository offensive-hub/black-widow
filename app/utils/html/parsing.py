import json
from html.parser import HTMLParser
from app.utils.requests import request, Type as RequestType

# Black Widow HTML Parser
class Parser(HTMLParser):
    relevant_tags = {
        'a': ['href'],                 # { 'href': 'https://...' }
        'form': ['action', 'method'],  # { 'action': 'https://...', 'method': 'GET', 'inputs': {'name': ['attr1', 'attr2']} }
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
        'script': ['src', 'data'],      # { 'src': '/some/script.js', 'data': 'function() ...' }
        'link': ['href'],               # { 'href': '*.xml' }
        'html': [],
        'body': []
    }
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
        #print('\n\n\nparent:')
        #print('len(self.queue_tag) = '+str(len(self.queue_tag)))
        #print(parent)

    def handle_starttag(self, tag, attrs):
        tag = str(tag).lower()
        #print(tag+' (start)')
        if ((not self.relevant) or tag in Parser.relevant_tags.keys()):
            tag_attrs={}
            for attr in attrs:
                attr_key = str(attr[0]).lower()
                attr_value = str(attr[1]).lower()
                if ((not self.relevant) or attr_key in Parser.relevant_tags.get(tag)):
                    tag_attrs[attr_key] = attr_value
            cur_tag = {'tag': tag, 'attrs': tag_attrs}
            self.queue_tag.append(cur_tag)
            #print('APPEND '+str(tag))
            if (tag in Parser.not_closed_tags): self.handle_endtag(tag)
        else:
            self.queue_tag_ignored.append(tag)

    def handle_endtag(self, tag):
        tag = str(tag).lower()
        #print(tag+' (end)')
        if (len(self.queue_tag_ignored) > 0 and tag == self.queue_tag_ignored[-1]):
            self.queue_tag_ignored.pop()
            return
        if (len(self.queue_tag) == 0): return
        cur_tag = self.queue_tag.pop()
        if (tag == cur_tag.get('tag')):
            self.__nest_tag__(cur_tag)
            #if (self.tags.get(tag) == None): self.tags[tag] = []
            #self.tags[tag].append(cur_tag)

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

# Printa il risultato delle funzioni @parse(url) e @relevant_parse(url)
def print_parsed(parsed, depth=0):
    space = ' ' * depth
    if (type(parsed) == dict):
        print(space + '{')
        for key, value in parsed.items():
            if (key == 'children'):
                print_parsed(value, depth+1)
            else:
                print((space*2) + key + ': ' + str(value))
        print(space + '}')
    elif (type(parsed) == list):
        for value in parsed: print_parsed(value, depth+1)
    else:
        raise('Invalid Argument: '+str(parsed))
