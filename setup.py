#!/usr/bin/env python
# -*- coding:utf-8 -*-

import io

from setuptools import setup


# NOTE(opessu) Subjective guidelines for Major.Minor.Micro ;)
#                Bumping Major means an API contract change.
#                Bumping Minor means API bugfix or new functionality.
#                Bumping Micro means CLI change of any kind unless it is
#                    significant enough to warrant a minor/major bump.
version = '0.0.5'

setup(name='python-veralite',
      version=version,
      description='Python API and command line tool for talking to the '
                  'Veralite™ Smart Home Controller',
      long_description=io.open('README.rst', encoding='UTF-8').read(),
      keywords='veralite',
      author='Okpe Pessu',
      author_email='opessu@zgreatone.net',
      url='https://github.com/zgreatone/python-veralite/',
      packages=['veralite'],
      install_requires=['simplejson==3.8.0', 'requests==2.20.0', 'configparser==3.5.0b2'],
      entry_points={
          'console_scripts': ['veralite=veralite.command_line:main'],
      },
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "Topic :: Utilities"
                   ]
      )
