from app.utils.html import form_parse, print_parsed
from app.utils.helpers.logger import Log


# Cerca dei form all'interno della pagina ritornata dall'url passato come parametro
# e li sfrutta tentando l'injection.
# @param url str L'url che restituisce l'html in cui trovare i form
# @param html str L'html in cui trovare i form
# @return
def inject_form(url=None, html=None):
    parsed_form = form_parse(url, html)
    Log.success('\n\n\nParsed Form:')
    print_parsed(parsed_form)
    # Log.error('NOT IMPLEMENTED: inject_form('+str(url)+', '+str(html)+')')


# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
# Se non lo trova, cerca un form in tutti i link con lo stesso dominio, presenti
# nella pagina ritornata dall'url. Tenta un'injection su tutti i form che trova.
# @param url str L'url che restituisce l'html in cui trovare i form
# @return
def deep_inject_form(url):
    Log.error('NOT IMPLEMENTED: deep_inject_form('+str(url)+')')
