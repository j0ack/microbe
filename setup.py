#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

__author__  = 'TROUVERIE Joachim'
__version__ = '1.0'
__appname__ = 'Microbe'


from setuptools import setup, find_packages

requirements = []
for line in open('REQUIREMENTS.txt', 'r'):
    requirements.append(line)

setup(
    name = __appname__,
    version = __version__,
    packages = find_packages(),
    author = __author__,
    author_email = 'joachim.trouverie@joacodepel.tk',
    description = 'Micro Blog Engine inspired by Pelican and powered by Flask',
    long_description = open('README.md').read(),
    install_requires = requirements,
    include_package_data=True,
    url='http://microbe.joacodepel.tk/',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points = {
        'console_scripts': [
            'microbe = microbe.views:main',
        ],
    },
)

