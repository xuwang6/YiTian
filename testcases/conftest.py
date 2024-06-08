#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : conftest.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 16:20
# Last Modified     : 2024/6/8 16:20
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import pytest


@pytest.fixture(scope="session", autouse=True)
def init_session():
    print("init_session begin!")
    yield
    print("init_session end!")


@pytest.fixture(scope="class", autouse=True)
def init_class():
    print("init_class begin!")
    yield
    print("init_class end!")


@pytest.fixture(scope="function", autouse=True)
def init_case():
    print("init_case begin!")
    yield
    print("init_case end!")
