import unittest2

import os
import time
import subprocess

from expresso import Cart, ShouldHaveFilesException

class TestRunCart(unittest2.TestCase):

    def setUp(self):
        self.cart = Cart()

        self.cart.load("""
          name: "Sample"
          files:
          - "assets/file.coffee"
          - "assets/folder/*"
          join: No
          """)

    def test_run_once(self):
        """
        Assure the cart has been ran 1 time.
        """
        self.assertEqual(self.cart.get_run_times(),1)

    def test_run_forever(self):
        """
        Assures the cart will run forever, since the watch flag
        has been passed by the order file.
        """
        self.cart.load("""
          watch: Yes
          name: "Sample"
          files:
          - "assets/file.coffee"
          - "assets/folder/*"
          deliver: "assets/delivery"
          join: No
          """)

        self.assertEqual(self.cart.get_run_times(),-1)

    def test_must_have_files(self):
        """
        Assures the cart will run forever, since the watch flag
        has been passed by the order file.
        """
        with self.assertRaises(ShouldHaveFilesException):
            self.cart.load("""                      
                      name: "Sample"           
                      deliver:
                      - "assets/delivery"
                      join: No
                      """)
            self.cart.run()

    def test_compiles_files(self):
        """
        Assures the files listed under files get compiled.
        """
        with self.assertRaises(OSError):
            os.path.getsize("tests/assets/file.js")

        self.cart.load("""
          name: "Sample"
          files:
          - tests/assets/file.coffee
          """)

        self.cart.run()
        time.sleep(1)
        self.assertTrue ( os.path.exists("tests/assets/file.js") )

    def test_compiles_folders(self):
        """
        Assures that folders listed under files get compiled
        if they have an /* after it's name.
        """

        with self.assertRaises(OSError):
            os.path.getsize("tests/assets/folder/1.js")
            os.path.getsize("tests/assets/folder/2.js")

        self.cart.load("""
          name: "Sample"
          files:
          - tests/assets/folder/*.coffee
          """)

        self.cart.run()
        time.sleep(1)
        self.assertTrue ( os.path.exists("tests/assets/folder/1.js") )
        self.assertTrue ( os.path.exists("tests/assets/folder/2.js") )

    def test_compiles_to_delivery_folder(self):
        """
        Assures that anything listed files get compiled to
        delivery folder.
        """

        with self.assertRaises(OSError):
            os.path.getsize("tests/assets/delivery/file.js")
            os.path.getsize("tests/assets/delivery/1.js")
            os.path.getsize("tests/assets/delivery/2.js")

        self.cart.load("""
          files:
          - tests/assets/folder/*.coffee
          - tests/assets/file.coffee
          deliver: tests/assets/delivery
          """)

        self.cart.run()
        time.sleep(1)

        self.assertTrue ( os.path.exists("tests/assets/delivery/file.js") )
        self.assertTrue ( os.path.exists("tests/assets/delivery/1.js") )
        self.assertTrue ( os.path.exists("tests/assets/delivery/2.js") )

    def test_joins(self):
        with self.assertRaises(OSError):
            os.path.getsize("tests/assets/joint.js")

        self.cart.load("""
          files:
          - tests/assets/folder/*.coffee
          - tests/assets/file.coffee
          deliver: tests/assets
          join: joint
          """)

        self.cart.run()
        time.sleep(1)

        self.assertTrue ( os.path.exists("tests/assets/joint.js") )

    def test_watches(self):
        """
        Assures the files listed are watched.
        """
        with self.assertRaises(OSError):
            os.path.getsize("tests/assets/watch/file.js")
            os.path.getsize("tests/assets/watch/1.js")
            os.path.getsize("tests/assets/watch/2.js")

        self.cart.load("""
          watch: Yes
          files:
          - tests/assets/folder/*.coffee
          - tests/assets/file.coffee
          deliver: tests/assets/watch
          """)

        self.cart.run()
        time.sleep(10)

        self.assertTrue ( os.path.exists("tests/assets/watch/file.js") )
        self.assertTrue ( os.path.exists("tests/assets/watch/1.js") )
        self.assertTrue ( os.path.exists("tests/assets/watch/2.js") )

