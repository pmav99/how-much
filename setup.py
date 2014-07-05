#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


def read_lines(filename):
    with open(filename, "rb", encoding="utf-8") as f:
        return f.readlines()


setup(
    name='bargain',
    version='0.1.0',
    description='Bargains from car.gr',
    author='Panos Mavrogiorgos',
    author_email='pmav99@gmail.com',
    url='http://bargain-pmav99.rhcloud.com/',
    install_requires=read_lines("requirements.txt")
)
