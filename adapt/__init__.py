__author__ = 'seanfitz'
import os
if os.path.exists('README.md'):
  import codecs
  __doc__ = codecs.open('README.md', encoding='utf-8', mode='r').read()

