import unittest

from xmlrunner import XMLTestRunner
import os
import sys

loader = unittest.TestLoader()
tests = loader.discover(os.path.dirname(os.path.realpath(__file__)), pattern="*Test.py")
fail_on_error = "--fail-on-error" in sys.argv
runner = XMLTestRunner()
result = runner.run(tests)
if fail_on_error and len(result.failures + result.errors) > 0:
    sys.exit(1)
