#!/usr/bin/python
"""
Build configuration for phishingline.

:Copyright:
    Copyright 2018 Lastline, Inc.  All Rights Reserved.
"""
from setuptools import setup

setup(
    name='phishingline',
    version="1.0.0",  # XXX: what scheme should we use for getting the version
    description='',
    url='https://gitlab.int.lastline.com/lastline/phishingline',
    author='Kabeer Vohra',
    author_email='kvohra@lastline.com',
    packages=['phishingline'],
    scripts=[],
    test_suite='nose.collector'
)
