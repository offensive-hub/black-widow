from app.env import APP_DEBUG
from app.utils.html import form_parse
from app.utils.helpers.logger import Log


# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
# @param url str L'url che restituisce l'html in cui trovare form e tentare
#        l'injection
# @param html str L'html contenente i form con cui tentare l'injection sui form trovati
# @return
def inject_form(url=None, html=None):
    Log.error('NOT IMPLEMENTED: inject_form('+str(url)+', '+str(html)+')')


# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
# Se non lo trova, o non riesce a fare l'injection, cerca un form in tutti i link
# con lo stesso dominio, presenti nella pagina ritornata dall'url
# @param url str L'url che restituisce l'html di cui l'injection sui form trovati
# @return
def deep_inject_form(url):
    Log.error('NOT IMPLEMENTED: deep_inject_form('+str(url)+')')
