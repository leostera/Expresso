"""
Expresso is a little Python continuous builder for CoffeeScript using PyV8.
"""

# The os module is used for retrieving files
import os
# multiprocessing.Process is used for watchers
import multiprocessing
# time for showing compile time
import time
# to load the latest coffee-script compiler
import urllib


# yaml is used to load the orders from files
from yaml import load
# import the Google V8 JavaScript Engine
import PyV8


class NoCodeToCompile(Exception):
    "Exception to arise when there is no code to be compiled."
    pass


class CompileException(Exception):
    "Exception to arise when there is an error in the compile process."
    pass


class V8CoffeeCompiler:
    """
    The PyV8 CoffeeScript compiler. Use it as base for your own compilers.
    """
    v8_context  = None
    v8_compiler = None
    compiled    = {}
    url         = None

    def __init__(self, latest=False):        
        """
        Init the PyV8 context and load the compiler either from CoffeeScript's
        Github repository or from a file.
        """        
        self.v8_context = PyV8.JSContext()
        self.v8_context.enter()
        if latest and self.url is not None:
            self.v8_compiler = self.v8_context.eval(
                                urllib.urlopen(self.url).read()
                                )
        else:
            coffee_script_file_d = os.open("coffee-script.js", os.O_RDONLY)            
            self.v8_compiler = self.v8_context.eval(
                                    os.read(coffee_script_file_d, 1000000000)
                                    )

    def compile(self, coffee=None):
        "Returns CoffeeScript code compiled to JavaScript"
        if coffee is None:
            raise NoCodeToCompile()
        return self.v8_compiler.compile(coffee)

    def get_version(self):
        "In this case, version is 1.2"
        if self.v8_compiler is not None:
            return (1, 2)
        return None


class CartIsEmptyError(Exception):
    "This exception will arise when trying to run the cart without loading it"
    pass


class ShouldHaveFilesError(Exception):
    "This exception will arise when trying to load an order without files"
    pass


class NullStreamError(Exception):
    "This exception will arise when trying to load an empty order"
    pass


class NoCompilerError(Exception):
    """
    This exception will arise from the compile method in the Cart class
    whenever it is executed without Cart.compiler being an actual Compiler.
    """
    pass


def change_ext(filepath):
    "Get the filepath for the compiled file"
    return "%s.js" % os.path.splitext(filepath)[0]


def get_src(filepath):
    "Get the source from a given file"
    with open(filepath, "r") as file_d:
        return file_d.read()

            
def save(content=None, dest=None):
    "Force saving a compiled file."
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    with open(dest, "w+") as file_d:
        file_d.write(str(content))
        file_d.flush()
        os.fsync()
        print "%s - compiled %s" % (time.strftime('%X'), dest)


class Cart:
    """
    The Cart that holds the commands, loads them and runs them.
    It pretty much does everything here.
    """

    order       = {}
    loaded      = False
    compiler    = None

    def __init__(self):
        self.order  = {}
        self.loaded = False
        self.compiler = V8CoffeeCompiler()

    def load(self, stream=None):
        "Loads a stream and parses it."
        if stream:
            self.order = load(stream)
            self.loaded = True
        else:
            self.order = {}
            self.loaded = False
            raise NullStreamError()

    def get_run_times(self):
        "Should it run forever or just once?"
        if self.order.get('watch') is True:
            return -1
        return 1

    def run(self):
        "Runs the cart"
        if self.order is {}:
            raise CartIsEmptyError()
        elif self.order.get('files') is None:
            raise ShouldHaveFilesError()
        else:

            if self.order.get('watch', False) is False:
                self.watch()
            else:
                self.build()            

    def compile(self, src):        
        "Get the compiled source code using the compiler at self.compiler"
        if self.compiler is None:
            raise NoCompilerError()
        else:
            compiled_src = None
            try:
                compiled_src = self.compiler.compile(src)
            except CompileException, exception:
                print "Error compiling: %s" % str(exception)
            return compiled_src

    def build(self):
        "Build the order based on it's configuration"
        # if no delivery specified
        if self.order.get('deliver', None) is None:
            # but files should be joined
            if self.order.get('join'):                        
                # compile self._join() and save it to 
                # a single file in the highest common folder
                # from all the files listed
                save(
                    self.compile(self._join()), 
                    os.path.join(
                        os.path.commonprefix( self.order.get('files') ), 
                        self.order.get('join')
                        )
                    )
            else:
                # compile each file into its folder
                for file_d in self.order.get('files'):
                    save(
                        self.compile( get_src(file_d) ), 
                        change_ext(file_d)
                        )

        else:
            if self.order.get('join'):
                # compile self._join() and save it to
                # a single file in the specified delivery folder
                save(
                    self.compile(self._join()), 
                    self._deliver_path(self.order.get('deliver'))
                    )
            else:
                # compile each file into the delivery folder
                # as separate js files
                for file_d in self.order.get('files'):
                    save(
                        self.compile( get_src(file_d) ), 
                        self._deliver_path(file_d)
                        )

    def watch(self):
        "Check for changes in the filepaths and re build if necessary"
        # do the watching here, as this is the process we will be threading
        process = multiprocessing.Process(kwargs={'shell':self.order.get('id')})
        process.start()
        process.join()
    
    def _deliver_path(self, filepath):
        "Get the delivery path for the compiled file"
        # Get the actual filename
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        # Return just the joined delivery path with the filename.js
        return os.path.join( "%s" % self.order.get('deliver'), 
            "%s.js" % filename)

    def _join(self):
        "Returns the joined source for all given files in an order."
        srcs_joined = None
        # get all the file descriptors
        file_ds = [os.open(f, os.O_RDONLY) for f
                in self.order.get('files')]
        if file_ds:
            # get all the sources
            srcs = [ os.read(file_d) for file_d in file_ds ]
            # and join them
            
            for src in srcs: # here
                srcs_joined += src + "\n" 

        for file_d in file_ds:
            file_d.close()

        return srcs_joined

################################################################################
#
# The actual runnable program starts below.
#
################################################################################

if __name__ == "__main__":

    print "I'll look for files in your 'orders' folder."

    ORDERS = os.listdir('orders')    
    CARTS = []

    for ORDER in ORDERS:
        CART = Cart()
        FILEDESCRIPTOR = os.open("orders/%s" % ORDER, os.O_RDONLY)
        CART.load( os.read(FILEDESCRIPTOR, 100000) )
        CARTS.append(CART)

    for CART in CARTS:
        CART.run()