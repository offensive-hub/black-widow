from threading import Thread


def multithreaded():
    jobs = []
    for i in xrange(0, threads):
        thread = Thread(target=func,args=(size,my_list[i]))
        jobs.append(thread)
    # Start the threads
    for j in jobs:
        j.start()
    # Ensure all of the threads have finished
    for j in jobs:
        j.join()

def simple():
    for i in xrange(0, threads):
        func(size,my_list[i])

def multiprocessed():
    processes = []
    for i in xrange(0, threads):
        p = Process(target=func,args=(size,my_list[i]))
        processes.append(p)
    # Start the processes
    for p in processes:
        p.start()
    # Ensure all processes have finished execution
    for p in processes:
        p.join()

if __name__ == "__main__":
    multithreaded()
    #simple()
    #multiprocessed()

class MyThread(Thread):
    index = 0
    def __init__(self, my_list):
        self.my_list = my_list
        self.name = '#'+str(MyThread.index++)
        Thread.__init__(self)
    def run(self):
        print ("Thread started")
        keys1 = {}
        for i in self.my_list:
            if (isfile('solved.key')): break
            header1 = encrypt_data('message: aaa', i).encode("hex")[0:18]
            keys1[header1] = i
            if (i % 10000 == 0): print(header1+': 0x%06x' % i)
        print "len(keys1):", len(keys1)
        in_file = open("encrypted", "r")
        data = ""
        while True:
            read = in_file.read(1024)
            if len(read) == 0:
                break
            data += read
        in_file.close()
        for i in self.my_list:
            if (isfile('solved.key')): break
            header1 = decrypt_data(data, i).encode("hex")[0:18]
            if (i % 10000 == 0): print(header1+': 0x%06x' % i)
            if header1 in keys1:
                print('Solved! key1: %06x key2: %06x' % (keys1[header1], i))
                with open('solved.key', 'w') as f:
                    f.write('Solved! Encode in hex the following keys:')
                    f.write('key1: ' + str(keys1[header1]))
                    f.write('key2: ' + str(i))
        print ("Thread end")

def main():
    n_procs = 2
    n_threads = 4
    threads = []
    my_list = range(0x000000, 0xFFFFFF)
    threads_list = (len(my_list) / n_threads) + (len(my_list) % n_threads)
    for i in range(n_threads):
        t = MyThread(my_list[(i*threads_list):((i+1)*threads_list)])
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
