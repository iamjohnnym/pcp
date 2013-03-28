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

        parser.add_argument('-c', '--cpu',
                    default=0,
                    type=int,
                    help='Specify the number of CPU cores to use')

        parser.add_argument('SOURCE',
                    nargs='+',
                    help='Source location')

        parser.add_argument('DIRECTORY',
                    nargs=1,
                    help='Directory location')

        self.args = parser.parse_args()

        self.root = self.args.SOURCE[0]

        root = self.root

        return self.args

    def check_path(self, path):
        """
        Verify the path exists
        """

        if os.path.exists(path):
            return True
        else:
            return False

    def get_files(self, path):
        """
        List files in the specified directory
        """

        test = []
        if os.path.isdir(path):
            for r, d, f in os.walk(os.path.dirname(path)):
                test.append({r: f})
            return test
        else:
            return 'false'

    def set_path(self, path):
        """
        Ensure the path is absolute
        """

        if '~' in path:
            return os.path.expanduser(path)
        else:
            return os.path.abspath(path)

    def build_path(self, li):
        """
        Build paths and place them in array which can be passed to the queue
        """

        self.paths = []
        self.queue = Queue()

        paths = self.paths
        #li == list : d == dict
        for self.d in li:
            for self.key, self.files in self.d.items():
                for self.file in self.files:
                    self.string = '{0}/{1}'.format(
                                    self.set_path(self.key),
                                    self.file)
                    self.queue.put(self.string)
        return self.queue

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

    def check_dir(self, dir_path):
        """
        Check if a dir exists and if is dir
        """

        try:
            os.makedirs(dir_path)
        except OSError:
            if not os.path.isdir(dir_path):
                raise

    def cp(self, queue, source, dest):
        """
        Handle the copying of files
        """

        while True:

            self.f = queue.get()

            #set abs pathing
            dest = self.set_path(dest)
            #change file path from original path to dest path
            self.dest_path = self.f.replace(source, dest)
            #ensure dir's exist and create it if not
            self.check_dir(os.path.dirname(self.dest_path))
            #shutil.copy for copying
            self.cpy = copy(self.f, self.dest_path)

            queue.task_done()

    def workers(self, queue, source, dest, cpus=0):
        """
        Create threads and copy
        """

        self.cores = self.get_num_cores()
        if cpus == 0:
            cpus = self.cores / 3
        elif cpus > self.cores:
            print "You can set a max of {0} CPU's to use.".format(self.cores)
            exit()

        print "Starting the copy with {0} threads.".format(cpus)

        for cpu in range(cpus):
            self.worker = Thread(target=self.cp, args=(queue, source, dest))
            self.worker.setDaemon(True)
            self.worker.start()

        queue.join()

if __name__ == '__main__':
    pcp = pcp()
    args = pcp.cli_params()
    pcp.workers(pcp.build_path(pcp.get_files(
                        args.SOURCE[0])),
                        pcp.set_path(args.SOURCE[0]),
                        args.DIRECTORY[0],
                        args.cpu)
