# Importo le variabili d'ambiente necessarie
from app.env import DEBUG

# TODO: Implementare classe Log, con: Log.info(...), Log.error(...)

# Fa eseguire al sistema operativo i comandi in args
# @param *args cmd [argomenti]
def pexec(*args):
    if (DEBUG):
        print('CALLED: pexec(*args)')
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
