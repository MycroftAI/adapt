__author__ = 'seanfitz'

from setuptools import setup

setup(
    name = "adapt-parser",
    version = "0.2.8",
    author = "Sean Fitzgerald",
    author_email = "sean@fitzgeralds.me",
    description = ("A text-to-intent parsing framework."),
    license = ("LGPL-3"),
    keywords = "natural language processing",
    url = "https://github.com/MycroftAI/adapt",
    packages = ["adapt", "adapt.tools", "adapt.tools.text"],

    install_requires = [
        "pyee==1.0.1",
        "six==1.10.0"
    ]
)
