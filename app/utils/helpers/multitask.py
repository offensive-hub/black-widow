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

import multiprocessing, threading, itertools, os
from app.utils.helpers.logger import Log

CPU = multiprocessing.cpu_count()

# Classe astratta, sfruttata sia da MultiThreading che da MultiProcessing
class __MultiTask__:
    MULTI_THREADING='MULTI_THREADING'
    MULTI_PROCESSING='MULTI_PROCESSING'

    # Sfrutta il multiprocessing o il multitasking per effettuare la stessa
    # operazione sugli elementi di un/una lista|tupla|dizionario|range.
    # Si assume che tutti gli argomenti di tipo lista|tupla|dizionario|range
    # debbano essere smistati ai vari processi
    # @param tasks_type __MultiTask__.MULTI_THREADING|__MultiTask__.MULTI_PROCESSING
    # @param target La funzione che i processi chiameranno
    # @param args Gli argomenti che verranno passati alla funzione
    # @param asynchronous True, se non bisogna attendere la fine dell'
    #                     esecuzione di tutti i tasks, False altrimenti
    # @param cpu Il numero di cpu da usare (default: il numero di cpu
    #            disponibili)
    def __start__(tasks_type, target=None, args=(), asynchronous=False, cpu=CPU):
        multiargs = (list, tuple, dict, range)  # I tipi di argomenti da dividere
        tasks = []
        def task_target(*args):
            if (tasks_type == __MultiTask__.MULTI_PROCESSING):
                tag = 'Process '
            else:
                tag = 'Thread '
            Log.info(tag + 'started')
            if (target != None): target(*args)
            Log.info(tag + 'end')
            #os._exit(0)
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
            if (tasks_type == __MultiTask__.MULTI_PROCESSING):
                task = multiprocessing.Process(target=task_target, args=task_args)
            else:
                task = threading.Thread(target=task_target, args=task_args)
            task.start()
            tasks.append(task)
        if (not asynchronous):
            # Attende la fine dell'esecuzione di tutti i tasks
            for task in tasks: task.join()

# Classe per il Multi Threading
class MultiThread(__MultiTask__):
    # Sfrutta il multithreading per effettuare la stessa operazione
    # sugli elementi di un/una lista|tupla|dizionario|range.
    # Si assume che tutti gli argomenti di tipo lista|tupla|dizionario|range
    # debbano essere smistati ai vari processi
    # @param target La funzione che i processi chiameranno
    # @param args Gli argomenti che verranno passati alla funzione
    # @param asynchronous True, se non bisogna attendere la fine dell'esecuzione di
    #                     tutti i processi, False altrimenti
    # @param cpu Il numero di cpu da usare (default: il numero di cpu disponibili)
    @staticmethod
    def start(target=None, args=(), asynchronous=False, cpu=CPU):
        __MultiTask__.__start__(__MultiTask__.MULTI_THREADING, target, args, asynchronous, cpu)

# Classe per il Multi Processing
class MultiProcess(__MultiTask__):
    # Sfrutta il multiprocessing per effettuare la stessa operazione
    # sugli elementi di un/una lista|tupla|dizionario|range.
    # Si assume che tutti gli argomenti di tipo lista|tupla|dizionario|range
    # debbano essere smistati ai vari processi
    # @param target La funzione che i processi chiameranno
    # @param args Gli argomenti che verranno passati alla funzione
    # @param asynchronous True, se non bisogna attendere la fine dell'esecuzione di
    #                     tutti i processi, False altrimenti
    # @param cpu Il numero di cpu da usare (default: il numero di cpu disponibili)
    @staticmethod
    def start(target=None, args=(), asynchronous=False, cpu=CPU):
        __MultiTask__.__start__(__MultiTask__.MULTI_PROCESSING, target, args, asynchronous, cpu)
