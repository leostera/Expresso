"""
NodeJS version of Expresso. Relies on a working Node.js installation along with
an available coffee script compiler that supports the --watch flag.
"""

# The os module is used for retrieving files
import os
# subprocess.Popen is used for one time calls
import subprocess
# multiprocessing.Process is used for watchers
import multiprocessing


# yaml is used to load the orders from files
from yaml import load


class CartIsEmptyError(Exception):
    "This exception will arise when trying to run the cart without loading it"
    pass


class ShouldHaveFilesError(Exception):
    "This exception will arise when trying to load an order without files"
    pass


class NullStreamError(Exception):
    "This exception will arise when trying to load an empty order"
    pass


class Cart:
    """
    Command holder and runner.
    """

    order   = {}
    loaded  = False

    def __init__(self):
        self.order = {}
        self.loaded = False

    def load(self, stream=None):
        "Loads a stream and parses it."
        if stream:
            self.order = load(stream)
            self.loaded = True
        else:
            self.order = {}
            self.loaded = False
            raise NullStreamError()

    def get_loaded(self):
        "Is an order loaded?"
        return self.loaded

    def get_order(self):
        "Get the current order."
        return self.order

    def get_run_times(self):
        "Should it run forever or just once?"
        if self.order.get('watch') is True:
            return -1
        return 1

    def run(self):
        "Run the cart"
        if self.order is {}:
            raise CartIsEmptyError()
        elif self.order.get('files') is None:
            raise ShouldHaveFilesError()
        else:
            for fname in self.order.get('files'):
                ## Copy the order details
                delivery_folder = self.order.get('deliver', "")
                should_watch    = self.order.get('watch', False)
                join_at         = self.order.get('join', False)

                cmd = "coffee -l"

                if should_watch is True:
                    cmd += "w"

                if join_at is not False:
                    cmd += " --join %s " % join_at

                if delivery_folder is not "":
                    cmd += " -o %s " % delivery_folder

                cmd += " -c %s " % fname

                if should_watch is False:
                    subprocess.Popen(cmd, shell=True)
                else:
                    multipro = multiprocessing.Process(target=subprocess.Popen,
                        args=(cmd,), kwargs={'shell':True})
                    multipro.start()
                    multipro.join()

################################################################################
#
# The actual runnable program starts below.
#
################################################################################

if __name__ == "__main__":

    print "I'll look for files in your 'orders' folder."

    ORDERS = os.listdir('orders')    
    CARTS = []

    for O in ORDERS:
        C = Cart()
        fd = os.open("orders/%s" % O, os.O_RDONLY)
        C.load( os.read(fd, 100000) )
        CARTS.append(C)

    for C in CARTS:
        C.run()