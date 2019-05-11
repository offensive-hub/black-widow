from app.env import APP_DEBUG
from app.utils.html import form_parse
from app.utils.helpers.logger import Log


# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
# e tenta l'injection sui form trovati all'interno dell'html
# @param url str L'url che restituisce l'html in cui trovare i form
# @param html str L'html in cui trovare i form
# @return
def inject_form(url=None, html=None):
    Log.error('NOT IMPLEMENTED: inject_form('+str(url)+', '+str(html)+')')


# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
# Se non lo trova, cerca un form in tutti i link con lo stesso dominio, presenti
# nella pagina ritornata dall'url
# @param url str L'url che restituisce l'html in cui trovare i form
# @return
def deep_inject_form(url):
    Log.error('NOT IMPLEMENTED: deep_inject_form('+str(url)+')')
