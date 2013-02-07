#!/usr/bin/env python

from threading import Thread
from Queue import Queue
from shutil import copy
import os


source = '/home/ecko/cptest/from'
dest = '/home/ecko/cptest/to'

num_threads = 5
queue = Queue()
files = os.listdir(source)

def pycp(i, q):
    """
    Copy files
    """
    while True:
        f = q.get()
        print "Thread {0}: Copying {1} to {2}".format(i, f, dest)
        cp_file = "{0}/{1}".format(source, f)
        cp = copy(cp_file, dest)

        #if cp == 0:
        #    print '{0}: is alive'.format(f)
        q.task_done()

for i in range(num_threads):
    worker = Thread(target=pycp, args=(i, queue))
    worker.setDaemon(True)
    worker.start()

for f in files:
    queue.put(f)
queue.join()
