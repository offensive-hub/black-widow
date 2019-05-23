"""
---- Multiprocessing ----

Il multiprocessing in Python è molto più veloce del multithreading, ma
occupa più risorse hardware, in quanto va a caricare in RAM molte parti del
programma uguali più volte (in base ai processi avviati)


---- Multithreading ----

Il multithreading in Python occupa meno risorse hardware del multiprocessing,
ma è più lento, in quanto forza un unico processo ad eseguire task paralleli
(come accade spesso in software provvisti di grafica)
"""

import multiprocessing, threading, itertools, os, signal, ctypes
from app.utils.helpers.logger import Log
from app.utils.helpers import storage
from app.env import APP_TMP

CPU = multiprocessing.cpu_count()

# Classe astratta, sfruttata sia da MultiThreading che da MultiProcessing
class MultiTask:
    MULTI_THREADING='MULTI_THREADING'
    MULTI_PROCESSING='MULTI_PROCESSING'
    tasks_types=(MULTI_THREADING, MULTI_PROCESSING)

    # @param tasks_type in MultiTask.tasks_types
    def __init__(self, tasks_type):
        if (tasks_type not in MultiTask.tasks_types):
            tasks_type = MultiTask.MULTI_PROCESSING
            Log.error(str(tasks_type)+' is not a valid tasks type!')
        self.tasks_type = tasks_type
        if (self.tasks_type == MultiTask.MULTI_PROCESSING):
            self.Multitask = multiprocessing.Process
            self.tag = 'Process '
        else:
            self.Multitask = threading.Thread
            self.tag = 'Thread '
        self.tasks = []
        pid = str(multiprocessing.process.current_process().pid)
        # File con pids (se multiprocessing)
        self.pidfile = APP_TMP + '/multitask.'+pid+'.pids'
        # File con result
        self.resfile = APP_TMP + '/multitask.'+pid+'.res'

    # Sfrutta il multiprocessing o il multitasking per effettuare la stessa
    # operazione sugli elementi di un/una lista|tupla|dizionario|range.
    # Si assume che tutti gli argomenti di tipo lista|tupla|dizionario|range
    # debbano essere smistati ai vari processi
    # @param target La funzione che i processi chiameranno
    # @param args Gli argomenti che verranno passati alla funzione
    # @param asynchronous True, se non bisogna attendere la fine dell'
    #                     esecuzione di tutti i tasks, False altrimenti
    # @param cpu Il numero di cpu da usare
    def start(self, target, args, asynchronous, cpu):
        self.tasks = []
        multiargs = (list, tuple, dict, range)  # I tipi di argomenti da dividere

        def task_target(*args):
            result = None
            if (self.tasks_type == MultiTask.MULTI_PROCESSING):
                curr_task = multiprocessing.process.current_process()
                Log.info(self.tag + 'started (PID='+str(curr_task.pid)+')')
            else:
                curr_task = threading.current_thread()
                Log.info(self.tag + 'started')
            if (target != None): result = target(*args)
            if (result != None):
                Log.info("Done! result: "+str(result))
                # Scrivo il risultato nel file
                Log.info('Writing result in '+str(self.resfile))
                storage.overwrite_file(str(result), self.resfile)
                # Termino tutti gli altri threads/processi
                if (self.tasks_type == MultiTask.MULTI_PROCESSING):
                    Log.info('Killing other processes')
                    pids = storage.read_file(self.pidfile).split(', ')
                    for pid in pids:
                        pid = int(pid)
                        if (pid == curr_task.pid): continue
                        try:
                            os.kill(pid, signal.SIGKILL)
                            Log.info('Process '+str(pid)+' killed!')
                        except Exception as e:
                            Log.error(str(e))
                    Log.info(self.tag + 'end')
                else:
                    Log.info('Ignoring other threads')
                    # Killa se stesso
                    pid = multiprocessing.process.current_process().pid
                    Log.info(self.tag + 'end')
                    os.kill(pid, signal.SIGKILL)

        for i in range(0, cpu):
            task_args = ()
            for arg in args:
                if (type(arg) in multiargs):
                    # Divido gli elementi in 1/cpu parti
                    p_list_len = (len(arg) / cpu) + (len(arg) % cpu)
                    if (type(arg) == dict):
                        iterator = iter(arg.items())
                        task_args += (dict(itertools.islice(iterator, int((i*p_list_len)), int((i+1)*p_list_len))),)
                    else:
                        task_args += (arg[int((i*p_list_len)):int(((i+1)*p_list_len))],)
                else: task_args += (arg,)
            task = self.Multitask(target=task_target, args=task_args)
            self.tasks.append(task)

        if (self.tasks_type == MultiTask.MULTI_PROCESSING):
            pids = []
            for task in self.tasks:
                task.start()
                pids.append(task.pid)
            storage.overwrite_file(str(pids).strip('[]'), self.pidfile)
        else:
            for task in self.tasks: task.start()

        if (not asynchronous):
            # Attende la fine dell'esecuzione di tutti i tasks
            for task in self.tasks:
                task.join()
                Log.info('Task '+str(task.name)+' joined')
            Log.info('Reading result in '+str(self.resfile))
            # Prendo il risultato dal file
            result = storage.read_file(self.resfile)
            # Elimino l'eventuale file con i pid
            storage.delete(self.pidfile)
            Log.info('MultiTask -> result: '+str(result))
            return result

        return None


# Crea un sottoprocesso che a sua volta genera n(=cpu) threads.
# La creazione del sottoprocesso è essenziale, in quanto il primo thread che
# riesce a trovare la soluzione, killerà il suo stesso processo, per interrompere
# anche tutti gli altri thread ed evitare attesa inutile.
# Sfrutta il multithreading per effettuare la stessa operazione
# sugli elementi di un/una lista|tupla|dizionario|range.
# Si assume che tutti gli argomenti di tipo lista|tupla|dizionario|range
# debbano essere smistati ai vari threads
# @param target La funzione che i threads chiameranno: se questa ritorna un valore
#               diverso da None, allora tutti i threads concorrenti verranno stoppati
# @param args Gli argomenti che verranno passati alla funzione
# @param asynchronous True, se non bisogna attendere la fine dell'esecuzione di
#                     tutti i threads, False altrimenti
# @param cpu Il numero di cpu da usare (default: il numero di cpu disponibili)
def multithread(target=None, args=(), asynchronous=False, cpu=CPU):
    multitask = MultiTask(MultiTask.MULTI_THREADING)
    # Gli argomenti da passare alla funzione multitask.start
    multithread_args = (target, args, asynchronous, cpu)
    return multiprocess(multitask.start, multithread_args, asynchronous=False, cpu=1)

# Sfrutta il multiprocessing per effettuare la stessa operazione
# sugli elementi di un/una lista|tupla|dizionario|range.
# Si assume che tutti gli argomenti di tipo lista|tupla|dizionario|range
# debbano essere smistati ai vari processi
# @param target La funzione che i processi chiameranno: se questa ritorna un valore
#               diverso da None, allora tutti i processi concorrenti verranno stoppati
# @param args Gli argomenti che verranno passati alla funzione
# @param asynchronous True, se non bisogna attendere la fine dell'esecuzione di
#                     tutti i processi, False altrimenti
# @param cpu Il numero di cpu da usare (default: il numero di cpu disponibili)
def multiprocess(target=None, args=(), asynchronous=False, cpu=CPU):
    multitask = MultiTask(MultiTask.MULTI_PROCESSING)
    return multitask.start(target, args, asynchronous, cpu)
