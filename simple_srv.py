#!/usr/bin/env python
# encoding: utf-8


"""
Create an XML-RPC Server that register several serices that run
in paralel in the background but can be invoked to know their state
"""


import multiprocessing
import time
import pickle
from SimpleXMLRPCServer import SimpleXMLRPCServer


class Service(multiprocessing.Process):
    """A service the increment a variable. """

    def __init__(self):
        """TODO: to be defined1. """
        multiprocessing.Process.__init__(self)
        self.count = 0

    def update_count(self):
        """ Update the counter """
        proc_name = multiprocessing.current_process().name
        print 'Doing something fancy in %s for %s!' % (proc_name, self.name)
        self.count += 1
        database = open('datafile.pkl', 'wb')
        pickle.dump(self.count, database)
        database.close()

    def run(self):
        """ Overloaded function provided by multiprocessing.Process.
            Called upon start() signal """
        end_time = time.time() + 120
        while time.time() < end_time:
            self.update_count()
            print self.count
            time.sleep(2)


def main():
    """ Main function """
    srv = Service()
    srv.start()

    def get_count():
        """Get state for the object"""
        database = open('datafile.pkl', 'rb')
        data = pickle.load(database)
        return data

    swift_srv = SimpleXMLRPCServer(('localhost', 9000), logRequests=True,
                                   allow_none=True)
    swift_srv.register_function(get_count)

    try:
        print 'Use Control-C to exit'
        swift_srv.serve_forever()
    except KeyboardInterrupt:
        print 'Exiting'

if __name__ == "__main__":
    main()
