#! /usr/bin/env python
# -*- coding : utf-8 -*-

from microbe import __version__
from setuptools import setup, find_packages

__author__ = 'TROUVERIE Joachim'
__appname__ = 'Microbe'


requirements = []
for line in open('REQUIREMENTS.txt', 'r'):
    requirements.append(line)

setup(
    name=__appname__,
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email='joachim.trouverie@joacodepel.tk',
    description='Micro Blog Engine inspired by Pelican and powered by Flask',
    long_description=open('README.rst').read(),
    install_requires=requirements,
    include_package_data=True,
    url='http://microbe.rtfd.org',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points={
        'console_scripts': [
            'microbe=microbe.commands:main',
        ],
    },
)
