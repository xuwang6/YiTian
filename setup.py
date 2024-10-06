#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: setup.py.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/9/7 15:22
"""

from setuptools import setup

setup(
    name='YiTian',
    version='1.0.0',
    author='xu wang',
    maintainer='xu wang',
    author_email='jason_wangxu@163.com',
    install_requires=[
        "requests",
        "urllib3",
    ],
    packages=['src'],
    # command_packages=['config', 'lib', 'logs', 'reports', 'resources', 'testcases'],
    py_modules=['run'],
    description="Android Performance Tool (support Python3)"
)
