from app.env import APP_DEBUG
from app.utils.html import form_parse
from app.utils.helpers.logger import Log


<<<<<<< HEAD
# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
# @param url str L'url che restituisce l'html in cui trovare form e tentare
#        l'injection
# @param html str L'html contenente i form con cui tentare l'injection sui form trovati
=======
# Cerca dei form all'interno della pagina ritornata dall'url passato come parametro
# e li sfrutta tentando l'injection.
# @param url str L'url che restituisce l'html in cui trovare i form
# @param html str L'html in cui trovare i form
>>>>>>> e947f04690749f6c0bc54ad72f575b79ba84976c
# @return
def inject_form(url=None, html=None):
    Log.error('NOT IMPLEMENTED: inject_form('+str(url)+', '+str(html)+')')


# Cerca un form all'interno della pagina ritornata dall'url passato come parametro
<<<<<<< HEAD
# Se non lo trova, o non riesce a fare l'injection, cerca un form in tutti i link
# con lo stesso dominio, presenti nella pagina ritornata dall'url
# @param url str L'url che restituisce l'html di cui l'injection sui form trovati
=======
# Se non lo trova, cerca un form in tutti i link con lo stesso dominio, presenti
# nella pagina ritornata dall'url. Tenta un'injection su tutti i form che trova.
# @param url str L'url che restituisce l'html in cui trovare i form
>>>>>>> e947f04690749f6c0bc54ad72f575b79ba84976c
# @return
def deep_inject_form(url):
    Log.error('NOT IMPLEMENTED: deep_inject_form('+str(url)+')')
