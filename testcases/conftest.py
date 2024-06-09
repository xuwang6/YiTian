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
from src.common import *


@pytest.fixture(scope="session", autouse=True)
def init_session():
    logger.debug("init_session begin!")
    yield
    logger.debug("init_session end!")


@pytest.fixture(scope="class", autouse=True)
def init_class():
    logger.debug("init_class begin!")
    yield
    logger.debug("init_class end!")


@pytest.fixture(scope="function", autouse=True)
def init_case(request):
    logger.debug(f"=>{request.function.__name__}")
    report_folder = os.path.join(RESOURCE_PATH, "%s_%s" % ({request.function.__name__}, {timestamp_ymd_hms()}))
    logger.debug(report_folder)
    create_folder(report_folder)
    yield
    print("case over!")
