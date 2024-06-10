#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : conftest.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 16:20
# Last Modified     : 2024/6/8 16:20
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import queue
import threading

import pytest

# from src.collect.collector_factory import CollectorFactory
from src.common import *

pkg = ""


@pytest.fixture(scope="session", autouse=True)
def init_session():
    logger.debug("init_session begin!")
    yield
    logger.debug("init_session end!")


@pytest.fixture(scope="class", autouse=True)
def init_class(request):
    logger.debug("init_class begin!")
    global pkg
    pkg = request.param
    yield
    logger.debug("init_class end!")


@pytest.fixture(scope="function", autouse=True)
def init_case(request):
    logger.debug(f"=>{request.function.__name__}")
    report_folder = os.path.join(REPORT_PATH, "%s_%s" % (request.function.__name__, timestamp_ymd_hms()))
    create_folder(report_folder)
    event = queue.Queue()
    # cpu_mem = CollectorFactory(device, core, pkg, report_folder, event)
    # cthread = threading.Thread(target=cpu_mem.collect_data("CPUMEM"))
    yield
    print("case over!")
