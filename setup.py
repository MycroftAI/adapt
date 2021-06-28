# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = 'seanfitz'

import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


def required(requirements_file):
    """Read requirements file and remove comments and empty lines."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_dir, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]

setup(
    name="adapt-parser",
    version="0.4.3",
    author="Sean Fitzgerald",
    author_email="sean@fitzgeralds.me",
    description=("A text-to-intent parsing framework."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=("Apache License 2.0"),
    keywords="natural language processing",
    url="https://github.com/MycroftAI/adapt",
    packages=["adapt", "adapt.tools", "adapt.tools.text"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    install_requires=required('requirements.txt')
)
