__author__ = 'seanfitz'

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "adapt-parser",
    version = "0.0.1",
    author = "Sean Fitzgerald",
    author_email = "sean@fitzgeralds.me",
    description = ("A text-to-intent parsing framework."),
    license = ("LGPL-3"),
    keywords = "natural language processing",
    url = "https://github.com/MycroftAI/adapt",
    packages = ["adapt"],
    long_description=read('README.md'),
    dependency_links = [
        "pyee"
    ]
)
