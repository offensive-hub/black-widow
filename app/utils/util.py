# Importo le variabili d'ambiente necessarie
from app.env import DEBUG, APP_LOGFILE
from app.utils.helpers.logger import Log

# Metodi

# Fa eseguire al sistema operativo i comandi in args
# @param *args cmd [argomenti]
def pexec(*args):
    if (DEBUG): Log.info('CALLED: pexec'+str(args))
    return
    """
    try:
        p=subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        Log.error(str(e))
        return []
    list_stdout=[]
    for line in p.stdout.readlines():
        list_stdout.append(str(line.decode('utf-8')).rstrip('\n'))
    return list_stdout
    """
