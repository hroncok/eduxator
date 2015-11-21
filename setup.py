#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='eduxator',
    version='0.0.1.dev1',
    description='Interactive command line interface for Edux classification',
    long_description=''.join(open('README.rst').readlines()),
    keywords='Edux, interface',
    author='Miro Hrončok',
    author_email='miro@hroncok.cz',
    license='MIT',
    packages=[p for p in find_packages() if p != 'test'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        ]
)
