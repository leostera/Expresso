import unittest

import os
import time

from expresso import V8CoffeeCompiler

class TestRunCart(unittest.TestCase):

    def setUp(self):
        self.v8 = V8CoffeeCompiler()