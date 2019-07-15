from urllib.parse import urlparse
from app.utils.html import form_parse, relevant_parse, find_forms, find_links
from app.utils.helpers.logger import Log
from app.utils.helpers.util import now, set_json
from app.env import APP_STORAGE_OUT
from app.utils.sql.sqlmapcli import SqlmapClient


def inject_form(url=None, html=None):
    """
    Search a form in the page returned by url (or inside the html).
    :param url: str The url to visit (or None)
    :param html: str the html code to analyze (or None)
    :return A list of parsed forms like [ form_1, form_2 ]
    """
    parsed_forms = dict()
    parsed_forms[url], cookies = form_parse(url, html)
    Log.success('Html parsed! Found '+str(len(parsed_forms[url]))+' forms')
    SqlmapClient.try_inject(parsed_forms, cookies)


def deep_inject_form(url, max_depth):
    """
    Search a form in the page returned by url.
    If it doesn't find a form, or the injection can't be done, it visit the website in search for other forms
    :param url: str The url to visit
    :param max_depth: int The max depth during the visit
    :return A dictionary of parsed forms like { '<url_visited>': [ form_1, form_2, ... }
    """
    base_url = urlparse(url).netloc
    parsed_forms = dict()
    out_file = APP_STORAGE_OUT + '/' + now() + '_DEEP_FORMS_' + base_url + '.json'

    def _deep_inject_form(href, depth=1):
        # Check the domain
        if href in parsed_forms or urlparse(href).netloc != base_url or (max_depth is not None and depth > max_depth):
            return

        # Visit the current href
        parsed_relevant, request_cookies = relevant_parse(href)
        parsed_forms[href] = find_forms(parsed_relevant, href)

        # Find adjacent links
        links = find_links(parsed_relevant)

        if len(parsed_forms) % 10 == 0:
            Log.info('Writing result in ' + out_file + '...')
            set_json(parsed_forms, out_file)

        # Visit adjacent links
        for link in links:
            # print('link: '+link)
            child_request_cookies = _deep_inject_form(link, depth+1)
            if request_cookies == '':
                request_cookies = child_request_cookies

        return request_cookies

    cookies = _deep_inject_form(url)

    Log.info('Writing result in ' + out_file + '...')
    set_json(parsed_forms, out_file)
    Log.success('Result wrote in ' + out_file)

    Log.success('Website crawled! Found '+str(len(parsed_forms))+' pages')

    SqlmapClient.try_inject(parsed_forms, cookies)

    return parsed_forms
