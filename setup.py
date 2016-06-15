from setuptools import setup
from adapt.util.setup_base import (
    find_all_packages,
    required,
    get_version
)
__author__ = 'seanfitz'

setup(
    name = "adapt-parser",
    version = "0.2.4",
    author = "Sean Fitzgerald",
    author_email = "sean@fitzgeralds.me",
    description = ("A text-to-intent parsing framework."),
    license = ("LGPL-3"),
    keywords = "natural language processing",
    url = "https://github.com/MycroftAI/adapt",
    #packages = ["adapt", "adapt.tools", "adapt.tools.text"],
    packages=find_all_packages("adapt"),
    install_requires=required('requirements.txt')
)
