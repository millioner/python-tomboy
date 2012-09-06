### -*- coding: utf-8 -*- ###
"""
Configuration file used by setuptools. It creates 'egg', install all dependencies.
"""

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#Dependencies - python eggs
install_requires = [
        'setuptools',
]

#Execute function to handle setuptools functionality
setup(name="python-tomboy",
    version="0.1",
    description="Tomboy integration library for Django framework",
    long_description=read('README.md'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    author='millioner',
    author_email='millioner.bbb@gmail.com',
    url='http://github.com/millioner/python-tomboy',
    classifiers=(
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ),
)
