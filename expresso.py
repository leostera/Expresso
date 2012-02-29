# The os module is used for retrieving files
import os
# subprocess.Popen is used for one time calls
import subprocess
# multiprocessing.Process is used for watchers
import multiprocessing
# yaml is used to load the orders from files
from yaml import load

################################################################################
#
#   Some exceptions
#
################################################################################
class CartIsEmpty(Exception):
    pass

class ShouldHaveFilesException(Exception):
    pass

################################################################################
#
#   The Cart that holds the commands, loads them and runs them.
#   It pretty much does everything here.
#
################################################################################
class Cart:
    """
    Command holder and runner.
    """

    order   = {}
    loaded  = False

    def load(self,stream=None):
        "Loads a stream and parses it."
        if stream:
            self.order = load(stream)
            self.loaded = True
        else:
            self.order = {}
            self.loaded = False
            raise "Null stream passed"

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
        if self.order is {}:
            raise CartIsEmpty()
        elif self.order.get('files') is None:
            raise ShouldHaveFilesException()
        else:
            for f in self.order.get('files'):
                ## Copy the order details
                delivery_folder = self.order.get('deliver', "")
                should_watch    = self.order.get('watch',False)
                join_at         = self.order.get('join',False)

                cmd = "coffee -l"

                if should_watch is True:
                    cmd += "w"

                if join_at is not False:
                    cmd += " --join %s " % join_at

                if delivery_folder is not "":
                    cmd += " -o %s " % delivery_folder

                cmd += " -c %s " % f

                if should_watch is False:
                    sp = subprocess.Popen(cmd,shell=True)
                else:
                    mp = multiprocessing.Process(target=subprocess.Popen, args=(cmd,),
                        kwargs={'shell':True})
                    mp.start()
                    mp.join()

################################################################################
#
# The actual runnable program starts below.
#
################################################################################

if __name__ == "__main__":
    """
    Load files from the orders directory and execute them.
    """
    print "I'll look for files in your 'orders' folder. Please place them all there"

    orders = os.listdir('orders')    
    carts = []

    for o in orders:
        c = Cart()
        fd = os.open("orders/%s" % o,os.O_RDONLY)
        c.load( os.read(fd,100000) )
        carts.append(c)

    for c in carts:
        c.run()