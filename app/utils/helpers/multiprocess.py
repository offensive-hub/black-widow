"""
Multiprocessing

Il multiprocessing in Python è molto più veloce del multithreading, ma
occupa più risorse hardware, in quanto va a caricare in RAM molte parti del
programma uguali più volte (in base ai processi avviati)
"""

import multiprocessing, itertools, os
from app.utils.helpers.logger import Log

CPU = multiprocessing.cpu_count()

# Sfrutta il multiprocessing per effettuare la stessa operazione
# sugli elementi di un/una lista|tupla|dizionario|range.
# Si assume che tutti gli argomenti di tipo lista|tupla|dizionario|range
# debbano essere smistati ai vari processi
# @param target La funzione che i processi chiameranno
# @param args Gli argomenti che verranno passati alla funzione
# @param asynchronous True, se non bisogna attendere la fine dell'esecuzione di
#                     tutti i processi, False altrimenti
# @param cpu Il numero di cpu da usare (default: il numero di cpu disponibili)
def start(target=None, args=(), asynchronous=False, cpu=CPU):
    multiargs = (list, tuple, dict, range)  # I tipi di argomenti da dividere
    processes = []
    def p_target(*args):
        tag = '[' + str(os.getpid()) + '] '
        Log.info(tag + 'Subprocess started')
        if (target != None): target(*args)
        Log.info(tag + 'Subprocess end')
    for i in range(0, cpu):
        p_args = ()
        for arg in args:
            if (type(arg) in multiargs):
                # Divido gli elementi in 1/cpu parti
                p_list_len = (len(arg) / cpu) + (len(arg) % cpu)
                if (type(arg) == dict):
                    iterator = iter(arg.items())
                    p_args += (dict(itertools.islice(iterator, int((i*p_list_len)), int((i+1)*p_list_len))),)
                else:
                    p_args += (arg[int((i*p_list_len)):int(((i+1)*p_list_len))],)
            else: p_args += (arg,)
        p = multiprocessing.Process(target=p_target, args=p_args)
        p.start()
        processes.append(p)
    if (not asynchronous):
        # Attende la fine dell'esecuzione di tutti i processi
        for p in processes: p.join()
