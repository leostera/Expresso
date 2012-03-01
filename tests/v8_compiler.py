import unittest2

import os
import time

from expresso import V8CoffeeCompiler

class TestRunCart(unittest2.TestCase):

    def setUp(self):
        self.v8 = V8CoffeeCompiler()