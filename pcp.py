#!/usr/bin/env python

from threading import Thread
from Queue import Queue
from shutil import copy
import os


class pcp():
    """
    Parallel Copy - A mutli-threaded copier
    """

    def __init__(self):
        """
        Initial menu and set variables
        """
        pass

    def cli_params(self):
        """
        CLI params for added features
        """

        try:
            import argparse
        except (ImportError, NotImplementedError):
            print 'Failed to import argparse module'
            exit(0)

        self.parser = argparse.ArgumentParser(
                    description='Parallel Copy - Copy multiple files at once',
                    )

        parser = self.parser

        parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='Enable Verbose Mode')

        parser.add_argument('SOURCE',
                    nargs='+',
                    help='Source location')

        parser.add_argument('DIRECTORY',
                    nargs='+',
                    help='Directory location')

        self.args = parser.parse_args()
        
        return self.args


    #check if path exists
    def check_path(self, path):
        """
        Verify the path exists
        """

        if os.path.exists(path):
            return True
        else:
            return False

    #get files from source dir
    def get_files(self, path):
        """
        List files in the specified directory
        """
        
        test = []
        if os.path.isdir(path):
            for r, d, f in os.walk(path):
                test.append({r: f})
            return test
        else:
            return 'false'
    
    def build_path(self, li):
        """
        Build paths and place them in array which can be passed to the queue
        """
        
        from Queue import Queue

        self.paths = []
        self.queue = Queue()

        paths = self.paths
        #li == list : d == dict
        for self.d in li:
            for self.key, self.files in self.d.items():
                for self.file in self.files:
                    self.string = '{0}/{1}'.format(self.key, self.file)
                    #paths.append(self.string)
                    self.queue.put(self.string)
        return self.queue

    #create thread count
    def get_num_cores(self):
        """
        Determine the number of cores on the current system
        """

        # Python 2.6+
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass
        
        # POSIX
        try:
            self.cores = int(os.sysconf('SC_NPROCESSORS_ONLN'))

            if self.cores > 0:
                return self.cores
        except (AttributeError, ValueError):
            pass

        # Windows
        try:
            self.cores = int(os.environ['NUMBER_OF_PROCESSORS'])

            if self.cores > 0:
                return self.cores
        except (KeyError, ValueError):
            pass

    def workers(self, queue, cpu=0):
        """
        Create threads and copy
        """
        
        from threading import Thread
        from shutil import copy
        if cpu == 0:
            cpu = self.get_num_cores() / 3
        elif (cpu > self.get_num_cores()):
            exit()

        while True:
            file = queue.get()


if __name__ == '__main__':
    pcp = pcp()
    args = pcp.cli_params()
    #li = pcp.get_files(args.SOURCE[0])
    #print os.listdir(args.SOURCE[0])
    #for x, y in enumerate(li):
    #    for foo, bar in y.items():
    #        print foo, bar
    pcp.workers(pcp.build_path(pcp.get_files(args.SOURCE[0])), 3)