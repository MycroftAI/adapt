import unittest

from xmlrunner import XMLTestRunner
import os

loader = unittest.TestLoader()
tests = loader.discover(os.path.dirname(os.path.realpath(__file__)), pattern="*Test.py")
runner = XMLTestRunner()
runner.run(tests)
