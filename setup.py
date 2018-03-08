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

from setuptools import setup

setup(
    name = "adapt-parser",
    version = "0.3.2",
    author = "Sean Fitzgerald",
    author_email = "sean@fitzgeralds.me",
    description = ("A text-to-intent parsing framework."),
    license = ("Apache License 2.0"),
    keywords = "natural language processing",
    url = "https://github.com/MycroftAI/adapt",
    packages = ["adapt", "adapt.tools", "adapt.tools.text"],

    install_requires = [
        "pyee==5.0.0",
        "six==1.10.0"
    ]
)
