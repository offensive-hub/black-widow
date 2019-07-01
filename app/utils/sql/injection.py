from urllib.parse import urlparse
from app.utils.html import form_parse, print_parsed, relevant_parse, find_forms, find_links
from app.utils.helpers.logger import Log
from app.utils.helpers.util import now, set_json
from app.env import APP_STORAGE_OUT


# Cerca dei form all'interno della pagina ritornata dall'url passato come parametro
# e li sfrutta tentando l'injection.
# @param url str L'url che restituisce l'html in cui trovare i form
# @param html str L'html in cui trovare i form
# @return
def inject_form(url=None, html=None):
    parsed_forms = form_parse(url, html)
    Log.success('Parsed Forms!')
    print_parsed(parsed_forms)
    Log.error('NOT IMPLEMENTED: inject_form('+str(url)+', '+str(html)+')')


# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
# Se non lo trova, cerca un form in tutti i link con lo stesso dominio, presenti
# nella pagina ritornata dall'url. Tenta un'injection su tutti i form che trova.
# @param url str L'url che restituisce l'html in cui trovare i form
# @return
def deep_inject_form(url):
    base_url = urlparse(url).netloc
    parsed_forms = dict()

    def _deep_inject_form(href):
        # Check the domain
        if href in parsed_forms or urlparse(href).netloc != base_url:
            return

        # Visit the current href
        parsed_relevant = relevant_parse(href)
        parsed_forms[href] = find_forms(parsed_relevant, href)

        # Find adjacent links
        links = find_links(parsed_relevant)

        # Visit adjacent links
        for link in links:
            # print('link: '+link)
            _deep_inject_form(link)

    _deep_inject_form(url)

    Log.success('Parsed Deep Forms!')
    out_file = APP_STORAGE_OUT + '/' + now() + '_deep_' + base_url + '.json'
    Log.info('Writing result in ' + out_file + '...')
    set_json(parsed_forms, url)
    # print_parsed(parsed_forms)

    Log.error('NOT IMPLEMENTED: deep_inject_form('+str(url)+')')

    return parsed_forms
