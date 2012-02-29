import unittest
from tests import yaml_to_cart, run_cart

def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(yaml_to_cart.TestYAMLToCart))
    suite.addTest(unittest.makeSuite(run_cart.TestRunCart))

    return suite

if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())