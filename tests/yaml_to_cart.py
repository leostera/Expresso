import unittest

from expresso_v8 import Cart

class TestYAMLToCart(unittest.TestCase):

    def setUp(self):
        self.cart = Cart()

        self.cart.load("""
          name: "Frappuccino, compressed, without lint."
          files:
          - "path1"
          - "path2"
          - "path3"
          deliver:
          - "delivery/path"
          join: No  
          compress: Yes
          lint: No
          """)

    def test_loaded_is_true_when_loaded(self):
        """
        Assures the cart has been loaded.
        """
        self.assertTrue(self.cart.loaded)

    def test_loaded_is_false_when_not_loaded(self):
        """
        Assures the cart hasn't been loaded.
        """
        self.cart = Cart()
        self.assertFalse(self.cart.loaded)

    def test_parsed(self):
        """
        Assures the cart has been parsed.
        """

        order = {
          "name": "Frappuccino, compressed, without lint.",
          "files": ["path1","path2","path3"],
          "deliver": ["delivery/path"],
          "join": False,
          "compress": True,
          "lint": False
          }

        self.assertEqual(self.cart.order,order)

###
# The tricky part is not the YAML.
###
